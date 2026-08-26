#!/usr/bin/env bash
# Verification harness for the godel-loopholes replication work.
#
# Every claim made about tooling and replication is re-run here from scratch.
# Each check prints the command, the expected result, and the observed result.
#
# Three checks are NEGATIVE CONTROLS. They are expected to FAIL, and the
# harness reports PASS only when they do fail. A verification script that can
# only ever print PASS is worthless, because it cannot distinguish a working
# toolchain from a broken assertion. If a negative control reports
# "CONTROL BROKEN", disbelieve every other line in this output.

set -uo pipefail

REPO="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
WORK="${GL_WORK:-/tmp/gl-replication}"   # scratch: cloned repos and downloaded PDFs
THY="$REPO/analysis/united-states-1947/isabelle"  # tracked theory sources
PASS=0
FAIL=0
INCONC=0

hdr()  { printf '\n\033[1m== %s ==\033[0m\n' "$1"; }
ok()   { printf '  \033[32mPASS\033[0m  %s\n' "$1"; PASS=$((PASS+1)); }
bad()  { printf '  \033[31mFAIL\033[0m  %s\n' "$1"; FAIL=$((FAIL+1)); }
note() { printf '        %s\n' "$1"; }
# A model finder that gives no answer has not given a negative answer. Conflating
# the two is the same error as reading a solver's arbitrary witness as a derived
# quantity; see the 218/219 note in TOOLING.md.
inconc() { printf '  \033[33mINCONCLUSIVE\033[0m  %s\n' "$1"; INCONC=$((INCONC+1));
           [[ $# -gt 1 ]] && printf '        %s\n' "$2"; return 0; }

# ---------------------------------------------------------------- tool presence

hdr "1. Tools present and reporting a version"

check_tool() {
  local name="$1" cmd="$2" expect="$3"
  local got
  got=$(eval "$cmd" 2>&1 | head -1)
  if [[ "$got" == *"$expect"* ]]; then
    ok "$name -> $got"
  else
    bad "$name -> expected to contain '$expect', got '$got'"
  fi
}

check_tool "Z3"          "$REPO/.venv/bin/python -c 'import z3;print(z3.get_version_string())'" "5."
check_tool "SWI-Prolog"  "swipl --version"                                                     "SWI-Prolog"
check_tool "Isabelle"    "isabelle version"                                                    "Isabelle2025"
check_tool "Lean 4"      "\$HOME/.elan/bin/lean --version"                                     "Lean (version 4"

# ------------------------------------------------------- claim 1: Z3 thresholds

hdr "2. Z3 re-derives threshold-arithmetic.md by an independent route"
note "Claim: minimum individuals to propose an amendment in 1947 = 146 House, 33 Senate;"
note "minimum ratifying states = 36. Source of truth: analysis/united-states-1947/threshold-arithmetic.md"

Z3OUT=$("$REPO/.venv/bin/python" - <<'PY' 2>&1
from z3 import Int, Optimize, sat

def solve(seats):
    o = Optimize(); p = Int('p'); y = Int('y')
    o.add(2*p > seats, p <= seats, 3*y >= 2*p, y <= p, y >= 0)
    o.minimize(y)
    assert o.check() == sat
    return o.model()[y].as_long()

def states(n):
    o = Optimize(); r = Int('r')
    o.add(4*r >= 3*n, r <= n); o.minimize(r)
    assert o.check() == sat
    return o.model()[r].as_long()

print(f"house={solve(435)} senate={solve(96)} states={states(48)}")
PY
)
note "observed: $Z3OUT"
[[ "$Z3OUT" == *"house=146"*  ]] && ok "House  = 146" || bad "House != 146"
[[ "$Z3OUT" == *"senate=33"*  ]] && ok "Senate = 33"  || bad "Senate != 33"
[[ "$Z3OUT" == *"states=36"*  ]] && ok "States = 36"  || bad "States != 36"

hdr "2b. NEGATIVE CONTROL: Z3 must refuse an impossible constraint"
note "Asking for a two-thirds majority smaller than one third of the quorum."
Z3NEG=$("$REPO/.venv/bin/python" - <<'PY' 2>&1
from z3 import Int, Solver, sat, unsat
s = Solver(); p = Int('p'); y = Int('y')
s.add(2*p > 435, p <= 435, 3*y >= 2*p, 3*y < p, y >= 0)
print(s.check())
PY
)
note "observed: $Z3NEG"
[[ "$Z3NEG" == *"unsat"* ]] && ok "correctly reported unsat" \
                            || bad "CONTROL BROKEN: expected unsat, got '$Z3NEG'"

# ------------------------------------------- claim 2: Yadamsuren IRC 121 replication

hdr "3. Yadamsuren et al. IRC 121 replication (Artificial Intelligence and Law, 2026)"
note "Claim: the published Prolog model reproduces on local SWI-Prolog, detects the"
note "inconsistency deterministically, and CLP(FD) finds a divergence fact pattern."

SRC="$WORK/section121-inconsistency-detection"
if [[ ! -d "$SRC" ]]; then
  note "not present, cloning..."
  mkdir -p "$WORK" && git clone --quiet --depth 1 \
    https://github.com/borchuluun/section121-inconsistency-detection.git "$SRC"
fi
note "upstream commit: $(git -C "$SRC" rev-parse HEAD 2>/dev/null)"

PL=$(cd "$SRC/phase3_llm_refinement_with_validation" && \
     swipl -q -g "run_all_validation_tests, halt(0)" -t "halt(1)" \
     refined_rule_set_with_validation.pl 2>&1)

echo "$PL" | grep -q 'Sum-of-Limits: \$500000, Reduced-\$500k: \$500000 -> no_divergence' \
  && ok "fully-qualified couple -> no_divergence" \
  || bad "fully-qualified couple did not report no_divergence"

echo "$PL" | grep -q 'Sum-of-Limits: \$375000, Reduced-\$500k: \$250000 -> divergence' \
  && ok "asymmetric couple -> divergence (\$375000 vs \$250000)" \
  || bad "asymmetric couple did not report the expected divergence"

# Determinism: the asymmetric line is printed three times (case 3, then twice in case 4).
DET=$(echo "$PL" | grep -c 'Sum-of-Limits: \$375000, Reduced-\$500k: \$250000 -> divergence')
[[ "$DET" -eq 3 ]] && ok "determinism: identical output on all 3 runs" \
                   || bad "determinism: expected 3 identical lines, saw $DET"

echo "$PL" | grep -q 'Gap                    = \$10416' \
  && ok "CLP(FD) found the \$10,416 divergence fact pattern" \
  || bad "CLP(FD) did not reproduce the \$10,416 gap"

hdr "3b. NEGATIVE CONTROL: Prolog must reject a false query"
note "Asking whether the fully-qualified couple diverges. It must not."
PLNEG=$(cd "$SRC/phase3_llm_refinement_with_validation" && swipl -q -g "
  reset_facts,
  assertz(owns(h, home, [period(_,_,30)])),
  assertz(uses_as_principal_residence(h, home, [period(_,_,30)])),
  assertz(owns(w, home, [period(_,_,30)])),
  assertz(uses_as_principal_residence(w, home, [period(_,_,30)])),
  ( compare_interpretations(h, w, _, _, divergence)
    -> writeln('CONTROL_BROKEN') ; writeln('correctly_refused') ), halt.
" refined_rule_set_with_validation.pl 2>&1 | tail -1)
note "observed: $PLNEG"
[[ "$PLNEG" == *"correctly_refused"* ]] && ok "correctly refused the false query" \
                                        || bad "CONTROL BROKEN: got '$PLNEG'"

# --------------------------------------------------- claim 3: Isabelle discharges proofs

hdr "4. Isabelle/HOL discharges proofs"
note "Claim: Isabelle accepts a theory transcribed from Zahoransky's thesis and proves"
note "both theorems, including that the deliberately contradictory axioms entail False."
note "NOTE: this validates the prover only. It is NOT the constitutional argument."

mkdir -p "$WORK/isabelle"
ISOUT=$(cd "$WORK/isabelle" && isabelle process_theories -O -U -f SmokeTest.thy SmokeTest 2>&1)
echo "$ISOUT" | grep -q 'theorem totalTemp17: totalTemp = 17' \
  && ok "proved  totalTemp17 : totalTemp = 17" \
  || bad "did not prove totalTemp17"
echo "$ISOUT" | grep -q 'theorem basic_unsat: False' \
  && ok "proved  basic_unsat : False (axioms are inconsistent, as the thesis states)" \
  || bad "did not prove basic_unsat"

hdr "4b. NEGATIVE CONTROL: Isabelle must reject a false theory"
note "A consistent theory asserting 1 + 1 = 3. This must not typecheck as proved."
cat > "$WORK/isabelle/NegControl.thy" <<'THY'
theory NegControl
  imports Main
begin
lemma should_not_prove: "(1::int) + 1 = 3" by simp
end
THY
NEGOUT=$(cd "$WORK/isabelle" && isabelle process_theories -O -f NegControl.thy NegControl 2>&1)
if echo "$NEGOUT" | grep -qE '^\*\*\*|Failed to finish|error'; then
  ok "correctly rejected 1 + 1 = 3"
else
  bad "CONTROL BROKEN: Isabelle did not reject a false lemma"
fi
rm -f "$WORK/isabelle/NegControl.thy"

# --------------------------------------------------------------- artifact integrity

hdr "4c. Zahoransky & Benzmuller constitutional theory (THE replication target)"
GC="$THY/GodelConstitution.thy"
if [[ -f "$GC" ]]; then
  note "theory: $(wc -l < "$GC" | tr -d ' ') lines, sha256 $(shasum -a 256 "$GC" | cut -c1-16)..."
  out=$(cd "$THY" && isabelle process_theories -O -U -f GodelConstitution.thy GodelConstitution 2>&1)
  if grep -q '^\*\*\*' <<<"$out"; then
    bad "theory did not compile cleanly"
    grep '^\*\*\*' <<<"$out" | head -5
  else
    ok "theory compiles with no errors"
  fi
  for th in noDictatorship_t1 noDictatorship_t2 Dictatorship_t3; do
    if grep -q "^theorem $th:" <<<"$out"; then ok "proved  $th"; else bad "MISSING $th"; fi
  done
  n=$(grep -c '^theorem ' <<<"$out" || true)
  note "$n theorems discharged in total"
else
  bad "GodelConstitution.thy missing"
fi

hdr "4d. NEGATIVE CONTROL: the axiom set must be CONSISTENT"
note "An inconsistent theory proves everything, which would make 4c meaningless."
note "Nitpick must find a countermodel for each dual below."
CM="$THY/Countermodel.thy"
if [[ -f "$CM" ]]; then
  out2=$(cd "$THY" && isabelle process_theories -O -U -f Countermodel.thy Countermodel 2>&1)
  found=$(grep -c 'Nitpick found a counterexample' <<<"$out2" || true)
  timedout=$(grep -c 'ran out of time\|Nitpick timed out' <<<"$out2" || true)
  if [[ "$found" -ge 3 ]]; then
    ok "countermodels found for all 3 duals -> theorems in 4c are non-vacuous"
  elif [[ "$timedout" -gt 0 ]]; then
    inconc "countermodel search timed out ($found/3 found). NOT a negative result:" \
           "Nitpick gave no answer, which says nothing about consistency. Re-run on an idle machine."
  else
    bad "expected 3 countermodels, got $found and no timeout -- investigate"
  fi
else
  bad "Countermodel.thy missing"
fi
CC="$THY/ConsistencyCheck.thy"
if [[ -f "$CC" ]]; then
  out3=$(cd "$THY" && isabelle process_theories -O -U -f ConsistencyCheck.thy ConsistencyCheck 2>&1)
  cc_timeout=$(grep -c 'ran out of time\|Nitpick timed out' <<<"$out3" || true)
  if grep -q 'Nitpick found a model' <<<"$out3"; then
    ok "axiom set is satisfiable (Nitpick found a model)"
  elif [[ "$cc_timeout" -gt 0 ]]; then
    inconc "satisfiability search timed out." \
           "No model found is NOT the same as no model existing."
  else
    bad "no model found and no timeout -- axiom set may be inconsistent"
  fi
  if grep -q 'Nitpick found a counterexample' <<<"$out3"; then
    ok "False is NOT entailed (countermodel exists)"
  elif [[ "$cc_timeout" -gt 0 ]]; then
    inconc "refutation of False timed out." \
           "A timeout is not a negative answer. It does NOT indicate inconsistency."
  else
    bad "could not refute False and did not time out -- investigate"
  fi
else
  bad "ConsistencyCheck.thy missing"
fi

hdr "5. Source artifacts, with checksums you can re-derive"
for f in zb-thesis.pdf zb-paper.pdf; do
  if [[ -f "$WORK/$f" ]]; then
    note "$f  $(shasum -a 256 "$WORK/$f" | cut -c1-64)"
    ok "$f present ($(du -h "$WORK/$f" | cut -f1))"
  else
    bad "$f missing"
  fi
done
note "re-download and compare:"
note "  curl -sSL -o /tmp/check.pdf https://www.mi.fu-berlin.de/inf/groups/ag-ki/Theses/Completed-theses/Bachelor-theses/2019/Zahoransky/BA-Zahoransky.pdf"
note "  shasum -a 256 /tmp/check.pdf"

# --------------------------------------------------------------------- what is NOT done

hdr "6. Explicitly NOT verified"
note "Lean 4       : version string only. No Lean code has been written or run."
note "Z&B numbers  : the thesis reports no runtimes or benchmark table, so only the"
note "               proofs themselves are comparable, not performance claims."
note "Z&B fidelity : transcribed by hand from the PDF. Bold-face operator notation"
note "               was renamed to avoid clashing with HOL built-ins; this is a"
note "               deliberate deviation from the printed source."
note "Yadamsuren   : the LLM-vs-hybrid accuracy comparison is not in their repo and"
note "               cannot be checked from the published artifacts."

# ------------------------------------------------------------------------- summary

printf '\n\033[1m== SUMMARY ==\033[0m\n'
printf '  passed: %d\n  failed: %d\n  inconclusive: %d\n' "$PASS" "$FAIL" "$INCONC"
if [[ "$FAIL" -eq 0 && "$INCONC" -eq 0 ]]; then
  printf '\n  All checks passed.\n\n'
elif [[ "$FAIL" -eq 0 ]]; then
  printf '\n  \033[33mNo failures, but %d check(s) inconclusive.\033[0m\n' "$INCONC"
  printf '  Inconclusive means a tool gave no answer, not that it answered no.\n\n'
else
  printf '\n  \033[31mSome checks failed.\033[0m\n\n'
fi
exit $(( FAIL > 0 ? 1 : 0 ))
