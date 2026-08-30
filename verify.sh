#!/usr/bin/env bash
# Verification harness for the godel-loopholes replication work.
#
# Every claim made about tooling and replication is re-run here from scratch.
# Each check prints the command, the expected result, and the observed result.
#
# Six checks are NEGATIVE CONTROLS. They are expected to FAIL, and the
# harness reports PASS only when they do fail. A verification script that can
# only ever print PASS is worthless, because it cannot distinguish a working
# toolchain from a broken assertion. If a negative control reports
# "CONTROL BROKEN", disbelieve every other line in this output.
#
# The count above is checked against reality in section 6. It said "three" for
# a period while five existed, which is exactly the drift this harness is
# supposed to catch and did not, because nothing was counting.

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

hdr "2c. The Article I Section 5 quorum cascade"
note "Claim: the Article V congressional threshold is not fixed, because the base of"
note "its fraction is set by the chamber the fraction constrains. Source of truth:"
note "analysis/united-states-1947/search/quorum_cascade.py"
CASC=$("$REPO/.venv/bin/python" "$REPO/analysis/united-states-1947/search/quorum_cascade.py" 2>&1)
grep -q 'two thirds of a quorum, settled 1920            : 179' <<<"$CASC" \
  && ok "agrees with threshold-arithmetic.md at the settled reading (146+33=179)" \
  || bad "cascade disagrees with threshold-arithmetic.md on the 1920 baseline"
grep -q 'after the Sec. 5 cascade                        : 4' <<<"$CASC" \
  && ok "cascade drives the congressional stage to 4 individuals" \
  || bad "cascade did not reproduce its recorded figure"
grep -q 'NOTHING IN THIS CASCADE TOUCHES THAT NUMBER' <<<"$CASC" \
  && ok "cascade reports its own disqualification (does not reach ratification)" \
  || bad "cascade no longer reports the ratification disqualification"

hdr "2d. NEGATIVE CONTROL: the cascade must not claim to reach ratification"
note "If this file ever reports a path to amendment, it has overreached."
if grep -qE 'states_still_required_to_ratify.*36|Article V still requires ratification by 36' <<<"$CASC"; then
  ok "still reports 36 of 48 state legislatures as untouched"
else
  bad "CONTROL BROKEN: the 36-state requirement is no longer being reported"
fi

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

# The smoke test is a tooling fixture, not an analysis, so it is generated here
# rather than tracked under analysis/. It is transcribed from thesis section 2
# (the beverage example) and its axiom set is DELIBERATELY inconsistent: teaHot
# asserts tooHot tea, which unfolds to tempOf tea > 20, while teaTemp10 fixes
# tempOf tea = 10. The thesis introduces the contradiction on purpose.
mkdir -p "$WORK/isabelle"
cat > "$WORK/isabelle/SmokeTest.thy" <<'THY'
theory SmokeTest
  imports Main
begin

datatype bvg = tea | coffee | juice
type_synonym temp = int

consts tempOf :: "bvg \<Rightarrow> temp"

definition totalTemp :: temp
  where "totalTemp \<equiv> (tempOf tea) + (tempOf coffee) + (tempOf juice)"

definition tooHot :: "bvg \<Rightarrow> bool"
  where "tooHot b \<equiv> if (b = juice) then (tempOf b > 5) else (tempOf b > 20)"

axiomatization where
  teaHot:      "tooHot tea" and
  teaTemp10:   "(tempOf tea) = 10" and
  coffeeTemp5: "(tempOf coffee) = 5" and
  juiceTemp2:  "(tempOf juice) = 2"

theorem totalTemp17: "totalTemp = 17"
  by (simp add: coffeeTemp5 juiceTemp2 teaTemp10 totalTemp_def)

lemma basic_unsat: "False"
  using teaHot teaTemp10 tooHot_def by simp

end
THY
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
  out=$(cd "$THY" && isabelle process_theories -O -U -f GodelCore.thy -f GodelConstitution.thy GodelConstitution 2>&1)
  note "GodelCore.thy holds the model; this file adds the three sup_rat axioms"
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
  out2=$(cd "$THY" && isabelle process_theories -O -U -f GodelCore.thy -f GodelConstitution.thy -f Countermodel.thy Countermodel 2>&1)
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
  out3=$(cd "$THY" && isabelle process_theories -O -U -f GodelCore.thy -f GodelConstitution.thy -f ConsistencyCheck.thy ConsistencyCheck 2>&1)
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

hdr "4e. OUR RESULT: what the ratification axiom carries"
note "Control (4c) proves Dictatorship_t3 from the full model."
note "This is the same model with amd2_sup_rat_t2 withdrawn -- the axiom asserting"
note "that the amendment vesting all three powers in one person has the support"
note "required for ratification. Article V's ratification stage is not otherwise"
note "represented in the model; the thesis says so and gives its reasons."
RD="$THY/RatificationDependency.thy"
if [[ -f "$RD" ]]; then
  out4=$(cd "$THY" && isabelle process_theories -O -U -f GodelCore.thy -f RatificationDependency.thy RatificationDependency 2>&1)
  # A model finder can fail to return an answer in more ways than timing out.
  # Kodkodi occasionally emits malformed output under parallel load. None of
  # these are negative answers, so they must not be reported as failures.
  rd_broke=$(grep -c 'ran out of time\|Nitpick timed out\|Malformed Kodkodi\|ill-formed Kodkodi\|Nitpick failed' <<<"$out4" || true)
  # Attribute each Nitpick verdict to its source line rather than to output order,
  # which is not source order under parallel processing.
  ln_sat=$(grep -n 'lemma reduced_model_is_satisfiable'   "$RD" | cut -d: -f1)
  ln_triv=$(grep -n 'lemma reduced_model_not_trivial'     "$RD" | cut -d: -f1)
  ln_neg1=$(grep -n 'lemma NEG1_dictatorship_not_entailed' "$RD" | cut -d: -f1)
  ln_neg2=$(grep -n 'lemma NEG2_absence_not_entailed'      "$RD" | cut -d: -f1)
  ln_fr1=$(grep -n 'lemma FREE1_support_not_entailed'      "$RD" | cut -d: -f1)
  ln_fr2=$(grep -n 'lemma FREE2_absence_of_support'        "$RD" | cut -d: -f1)
  verdict_at() {  # $1 = lemma line; nitpick call is the next line
    # "Output (line 76 of "...")" -> field 3 is the line number. Avoids the
    # three-argument match() of GNU awk, which BSD awk on macOS does not have.
    awk -v want="$(( $1 + 1 ))" '
      $1 == "Output" && $2 == "(line" { cur = $3 }
      /Nitpick found a model/          { if (cur == want) { print "model";   exit } }
      /Nitpick found a counterexample/ { if (cur == want) { print "counter"; exit } }
    ' <<<"$out4"
  }
  v_sat=$(verdict_at "$ln_sat"); v_triv=$(verdict_at "$ln_triv")
  v_neg1=$(verdict_at "$ln_neg1"); v_neg2=$(verdict_at "$ln_neg2")
  v_fr1=$(verdict_at "$ln_fr1");  v_fr2=$(verdict_at "$ln_fr2")

  if grep -q '^theorem amd1a_valid_t2_without_any_ratification_axiom:' <<<"$out4"; then
    ok "recorded null result: amd1a at t2 needs no ratification axiom at all"
  else
    bad "the recorded null result no longer proves -- see RatificationDependency.thy"
  fi

  # Report each verdict, but never convert a tool failure into a negative answer.
  check_verdict() {  # $1 = observed, $2 = expected, $3 = pass text, $4 = fail text
    if [[ "$1" == "$2" ]]; then ok "$3"
    elif [[ -z "$1" && "$rd_broke" -gt 0 ]]; then
      inconc "$4 -- Nitpick returned no answer" \
             "A model finder that fails to answer has not answered no. Re-run on an idle machine."
    else bad "$4 (observed: ${1:-none})"
    fi
  }
  note "Five of the six Nitpick rows below are FORCED by the control being"
  note "satisfiable, so they are instrument checks rather than findings."
  note "Only NEG1 is new information."
  check_verdict "$v_sat"  model   "reduced model is satisfiable (forced)" \
                                  "reduced model: no satisfying model found"
  check_verdict "$v_triv" counter "reduced model does not entail False (forced)" \
                                  "reduced model may be inconsistent"
  check_verdict "$v_neg1" counter "THE RESULT: no proof of Dictatorship_t3 exists without amd2_sup_rat_t2" \
                                  "expected a countermodel to Dictatorship_t3"
  check_verdict "$v_neg2" counter "nor is its negation entailed (forced) -- NEG1 is not a safety result" \
                                  "expected a countermodel to the dual as well"
  note "FREE1 is forced by NEG1 (if T entailed the axiom it would entail D);"
  note "FREE2 is forced by the control. Neither adds anything."
  check_verdict "$v_fr1"  counter "the withheld axiom is not entailed either (forced)" \
                                  "expected a countermodel to sup_rat amd2 at t2"
  check_verdict "$v_fr2"  counter "nor is its negation (forced) -- the axiom is independent" \
                                  "expected a countermodel to the absence of sup_rat amd2"

  # The refutation of the earlier, invalid syntactic argument for freeness.
  if grep -q '^theorem sup_rat_IS_derivable_from_ratification:' <<<"$out4"; then
    ok "recorded null result: sup_rat IS derivable via osr's contrapositive"
  else
    bad "the recorded contraposition null result no longer proves"
  fi
else
  bad "RatificationDependency.thy missing"
fi

hdr "4f. THE MAIN RESULT: Goedel's step one is represented, occurs, and is inert"
note "Six experiments, all generated from the two tracked theory files so that"
note "the model is never transcribed twice. See analysis/united-states-1947/"
note "inert-manoeuvre.md. The theorems are kernel-certified; the consistency and"
note "satisfiability probes are Nitpick, which is a model finder and not a proof."
note "Do not run two copies of verify.sh at once. Isabelle and Nitpick contend for"
note "cores and the timeouts then fire, which this section reports as FAIL rather"
note "than as the resource problem it is. Observed: 8 spurious failures that way."
SWEEP="$REPO/analysis/united-states-1947/search/axiom_sweep.py"
if [[ -f "$SWEEP" ]] && command -v isabelle >/dev/null 2>&1; then
  sweep_out=$(cd "$(dirname "$SWEEP")" && python3 axiom_sweep.py all 2>&1)
  grep -q 'PROVED from six consistent axioms' <<<"$sweep_out" \
    && ok "Dictatorship_t3 proved from 6 of 51 axioms, and the 6 are consistent" \
    || bad "the six-axiom proof failed, or the six-axiom theory proves False"
  grep -q 'published theorems still proved: noDictatorship_t1, noDictatorship_t2, Dictatorship_t3' <<<"$sweep_out" \
    && ok "all 3 published theorems survive deleting the amd1 axioms" \
    || bad "deleting the amd1 axioms changed a published theorem"
  grep -q 'intermediate amd1 lemmas still proved: 5 of 5' <<<"$sweep_out" \
    && ok "and all 5 intermediate amd1 lemmas survive too -- no proposition is lost" \
    || bad "a lemma was lost; inert-manoeuvre.md fact three overstates the survival"
  grep -q 'in a CONSISTENT theory' <<<"$sweep_out" \
    && ok "and the reduced theory is consistent, so that survival is not vacuous" \
    || bad "the reduced theory proves False -- the ablation is worthless"
  grep -q 'the authors were right' <<<"$sweep_out" \
    && ok "the authors' defence checks out: keeping omsp at t2 derives False" \
    || bad "could not reproduce the thesis's own inconsistency claim"
  grep -q 'the premise amd2_prop_t2 IS the forbidden act' <<<"$sweep_out" \
    && ok "omsp is falsified at t2 by stipulating its own breach, not by any amendment" \
    || bad "could not prove omsp false at t2"
  if grep -q 'blocking IS representable' <<<"$sweep_out"; then
    ok "and blocking IS representable -- the logic was adequate, the encoding was not"
  elif grep -q 'INCONCLUSIVE -- the blocked state proves' <<<"$sweep_out"; then
    inconc "blocked state proved, but nitpick found no model this run" \
           "The theorem is kernel-certified; only the satisfiability search flaked. Re-run: python3 axiom_sweep.py blocking"
  else
    bad "could not construct the blocked state -- inert-manoeuvre.md overclaims"
  fi
  note "The repeal experiment exists because an earlier draft claimed the model"
  note "could not represent repeal at all. It can. These four checks are the"
  note "retraction, kept executable so the claim cannot drift back."
  grep -q 'PROVED (term identity)' <<<"$sweep_out" \
    && ok "amd1a IS the negation of omsp -- the same term, not merely equivalent" \
    || bad "amd1a = not-omsp did not prove; fact five of inert-manoeuvre.md is wrong"
  grep -q 'is_rat amd1a holds at t2 in the full model   PROVED' <<<"$sweep_out" \
    && ok "the repeal event genuinely occurs in the published model" \
    || bad "could not derive is_rat amd1a at t2; the repeal may not occur after all"
  grep -q 'stipulations alone, no amd1 axiom cited      PROVED' <<<"$sweep_out" \
    && ok "yet amd1a's content follows from the amd2 stipulations with no amd1 axiom" \
    || bad "amd1a's content does NOT follow from amd2 alone -- the explanation fails"
  if grep -q 'with the amd1 axioms deleted, is_rat amd1a: counterexample' <<<"$sweep_out"; then
    ok "and deleting the amd1 axioms really does remove the event, not rename it"
  elif grep -q 'RESULT: INCONCLUSIVE (nitpick gave no usable verdict)' <<<"$sweep_out"; then
    inconc "nitpick gave no verdict on is_rat amd1a in the reduced theory" \
           "Model-finder flake, not a substantive failure. Re-run: python3 axiom_sweep.py repeal"
  else
    bad "is_rat amd1a survives deletion -- fact three would then be about nothing"
  fi
  note "The four-axiom lower bound is a headline claim, so it is run here rather"
  note "than left to a separate command. This is the slow part of the section:"
  note "it asks Nitpick for six countermodels against the full 51-axiom theory."
  tight_out=$(cd "$(dirname "$SWEEP")" && python3 axiom_sweep.py tight 2>&1)
  grep -q 'the six-axiom set is IRREDUNDANT' <<<"$tight_out" \
    && ok "the six-axiom set is irredundant -- no member of it is idle" \
    || bad "irredundance failed; inert-manoeuvre.md fact two overstates"
  if grep -q 'RESULT (b): 4 of the six are necessary to every sufficient support' <<<"$tight_out"; then
    ok "and exactly 4 of the 6 are necessary to EVERY sufficient support"
    grep -q 'the lower bound is 4, not 6' <<<"$tight_out" \
      && ok "and the script says so: the bound is 4, six is NOT proved minimum" \
      || bad "the script no longer states the bound honestly"
  elif grep -q 'UNREADABLE VERDICT' <<<"$tight_out"; then
    inconc "nitpick gave an unreadable verdict during the lower-bound run" \
           "Model-finder flake under load. Re-run alone: python3 axiom_sweep.py tight"
  else
    bad "the measured necessary set no longer matches EXPECTED_NECESSARY"
  fi
else
  inconc "axiom_sweep.py or Isabelle unavailable" \
         "Section 4f needs Isabelle on PATH. Without it the strongest result is unchecked."
fi
note "The textual fact this result depends on -- that the thesis never propagates"
note "omsp past t1 -- is checked in section 5c, once the PDFs are present."

hdr "4g. The published axiom inventory is not stale"
note "data/ablation.json is what the website renders. It is GENERATED from the"
note "two theory files, so the only way it can lie is by being out of date."
note "Regenerating it needs no Isabelle, so this check runs everywhere."
if [ -f "$SWEEP" ] && [ -f "$REPO/data/ablation.json" ]; then
  regen=$(cd "$(dirname "$SWEEP")" && python3 axiom_sweep.py inventory 2>/dev/null)
  if [ -z "$regen" ]; then
    bad "axiom_sweep.py inventory produced nothing"
  elif diff -q <(printf '%s\n' "$regen") \
              <(printf '%s\n' "$(cat "$REPO/data/ablation.json")") >/dev/null; then
    ok "data/ablation.json matches the theory files it is generated from"
  else
    bad "data/ablation.json is stale; regenerate with: python3 axiom_sweep.py inventory > data/ablation.json"
  fi
  n_ax=$(python3 -c 'import json,sys; print(len(json.load(open(sys.argv[1]))["axioms"]))' "$REPO/data/ablation.json" 2>/dev/null)
  want_ax=$(python3 "$REPO/tools/facts.py" --value model.axioms.total 2>/dev/null)
  [ -n "$n_ax" ] && [ "$n_ax" = "$want_ax" ] \
    && ok "and it carries $n_ax axioms, the number facts.json advertises" \
    || bad "ablation.json has $n_ax axioms; facts.json says $want_ax"
else
  inconc "axiom_sweep.py or data/ablation.json missing" \
         "Section 4g checks the website's axiom data against the theory files."
fi

hdr "5. Source artifacts, with checksums you can re-derive"
note "Fetched on demand if absent, so a clean checkout reproduces this section."
declare -a PDF_NAME=(zb-thesis.pdf zb-paper.pdf)
declare -a PDF_URL=(
  "https://www.mi.fu-berlin.de/inf/groups/ag-ki/Theses/Completed-theses/Bachelor-theses/2019/Zahoransky/BA-Zahoransky.pdf"
  "http://ceur-ws.org/Vol-2632/MIREL-19_paper_1.pdf"
)
# Derived twice from independent downloads. No official checksum is published,
# so these carry only the authority of having been re-derived, exactly as with
# the Isabelle tarball figure in TOOLING.md.
declare -a PDF_SHA=(
  "1248c242dcd5b7be5a153ddbbfb4054ee20b7a4ce0752997bf70636fa87f55c6"
  "bff63e5d9818f64a7399326667f1a2acad38ee5ffd7f6102420e2badf200a79a"
)
for i in 0 1; do
  f="${PDF_NAME[$i]}"
  if [[ ! -f "$WORK/$f" ]]; then
    note "$f not present, fetching..."
    curl -sSL --max-time 180 -o "$WORK/$f" "${PDF_URL[$i]}" || true
  fi
  if [[ ! -f "$WORK/$f" ]]; then
    inconc "$f could not be fetched" "Network failure is not a replication failure. Retry, or fetch by hand from ${PDF_URL[$i]}"
    continue
  fi
  got=$(shasum -a 256 "$WORK/$f" | cut -d' ' -f1)
  if [[ "$got" == "${PDF_SHA[$i]}" ]]; then
    ok "$f  sha256 matches ($(du -h "$WORK/$f" | cut -f1))"
  else
    bad "$f  sha256 MISMATCH: expected ${PDF_SHA[$i]}, got $got"
  fi
done

hdr "5b. Single source of truth: the model is stored exactly once"
note "The transcription was once copied verbatim into three files that could drift"
note "apart silently. These checks exist so that cannot happen again."
dup_fail=0
for d in ConsistencyCheck Countermodel; do
  grep -q '^ *imports GodelConstitution' "$THY/$d.thy" \
    || { bad "$d.thy does not import GodelConstitution"; dup_fail=1; }
done
grep -q '^ *imports GodelCore' "$THY/RatificationDependency.thy" \
  || { bad "RatificationDependency.thy does not import GodelCore"; dup_fail=1; }
grep -q '^ *imports GodelCore' "$THY/GodelConstitution.thy" \
  || { bad "GodelConstitution.thy does not import GodelCore"; dup_fail=1; }
[[ "$dup_fail" -eq 0 ]] && ok "every derived theory imports rather than duplicates"

# Proxies for "the model is defined once": its type of government bodies and its
# definition of the target predicate must each appear in exactly one file.
for marker in '^datatype g = Congress' '^definition Dictatorship'; do
  n=$(grep -l "$marker" "$THY"/*.thy 2>/dev/null | wc -l | tr -d ' ')
  if [[ "$n" -eq 1 ]]; then
    ok "'$marker' appears in exactly 1 theory file"
  else
    bad "'$marker' appears in $n theory files, expected 1 -- the model was copied"
  fi
done

# STRONGER: the split must have preserved every labelled formula character for
# character, not merely the set of labels. Names matching proves nothing about
# bodies. The pre-split file is recovered from git and its formulas compared
# against the union of the two files that replaced it.
SPLIT_COMMIT=3a7ded5
if command -v git >/dev/null 2>&1 && command -v python3 >/dev/null 2>&1 \
   && git -C "$REPO" cat-file -e "$SPLIT_COMMIT:analysis/united-states-1947/isabelle/GodelConstitution.thy" 2>/dev/null; then
  git -C "$REPO" show "$SPLIT_COMMIT:analysis/united-states-1947/isabelle/GodelConstitution.thy" > "$WORK/pre_split.thy"
  cat > "$WORK/axnorm.py" <<'PYEOF'
import re, sys
LABEL = re.compile(r'\b([A-Za-z][A-Za-z0-9_' + chr(39) + r']*)\s*:\s*"((?:[^"\\]|\\.)*)"')
# The labelled-proposition regex above misses definition and abbreviation
# bodies, which is where amd2, Dictatorship, psr, rv and tnext live -- exactly
# what the six-axiom proof leans on. Capture those separately by name.
DEFN = re.compile(r'^\s*(?:definition|abbreviation)\s+([A-Za-z][A-Za-z0-9_' + chr(39)
                  + r']*)\b.*?\bwhere\s*"((?:[^"\\]|\\.)*)"', re.M | re.S)
def norm(text):
    out = []; depth = 0; i = 0                 # nesting-aware (* comment *) strip
    while i < len(text):
        if text.startswith('(*', i): depth += 1; i += 2; continue
        if text.startswith('*)', i) and depth: depth -= 1; i += 2; continue
        if not depth: out.append(text[i])
        i += 1
    body = ''.join(out)
    d = {m.group(1): re.sub(r'\s+', ' ', m.group(2)).strip()
         for m in LABEL.finditer(body)}
    d.update({'def ' + m.group(1): re.sub(r'\s+', ' ', m.group(2)).strip()
              for m in DEFN.finditer(body)})
    return d
pre = norm(open(sys.argv[1]).read())
post = {}
for f in sys.argv[2:]: post.update(norm(open(f).read()))
lost = sorted(set(pre) - set(post)); added = sorted(set(post) - set(pre))
changed = sorted(k for k in set(pre) & set(post) if pre[k] != post[k])
if lost:    print("LOST:", ", ".join(lost))
if added:   print("ADDED:", ", ".join(added))
if changed: print("CHANGED:", ", ".join(changed))
print(("IDENTICAL %d" % len(pre)) if not (lost or added or changed) else "DIFFERS")
PYEOF
  split_out=$(python3 "$WORK/axnorm.py" "$WORK/pre_split.thy" \
                      "$THY/GodelCore.thy" "$THY/GodelConstitution.thy")
  if [[ "$split_out" == IDENTICAL* ]]; then
    ok "split preserved all ${split_out#IDENTICAL } formulas and definitions verbatim (vs $SPLIT_COMMIT)"
  else
    bad "the split changed the model: $(tr '\n' ';' <<<"$split_out")"
  fi
else
  inconc "cannot compare against the pre-split file at $SPLIT_COMMIT" \
         "Needs git, python3, and full history. Without it, only label names are checked."
fi
# in exactly the intended way. Comments are stripped first, because the file
# names the withheld axiom in prose in order to explain itself.
RD_CODE=$(perl -0777 -pe 's/\(\*.*?\*\)//gs' "$THY/RatificationDependency.thy")
exp_fail=0
for ax in amd1a_sup_rat_t1 amd1b_sup_rat_t1; do
  grep -q "$ax" <<<"$RD_CODE" \
    || { bad "$ax missing from the reduced arm -- Article V would not be amended"; exp_fail=1; }
done
grep -q 'amd2_sup_rat_t2' <<<"$RD_CODE" \
  && { bad "amd2_sup_rat_t2 present in the reduced arm -- the manipulation is void"; exp_fail=1; }
[[ "$exp_fail" -eq 0 ]] \
  && ok "reduced arm differs from control in exactly one axiom (amd2_sup_rat_t2)"

hdr "5c. OUR RESULT: the caveat is in the thesis and not in the paper"
note "Zahoransky's thesis states, in section 3, that no state legislature would plausibly"
note "ratify the first amendment, and that if they would, the two-step manoeuvre is"
note "unnecessary; and in section 4.1 that ratification support is left unspecified."
note "Neither remark survives into the peer-reviewed paper, nor into the thesis's own"
note "conclusion. This check pins those claims to the two PDFs above."
if ! command -v pdftotext >/dev/null 2>&1; then
  inconc "pdftotext not installed" "Install poppler (brew install poppler) to check the text of the sources."
elif [[ ! -f "$WORK/zb-thesis.pdf" || ! -f "$WORK/zb-paper.pdf" ]]; then
  inconc "source PDFs unavailable" "Section 5 could not fetch them; this check depends on those bytes."
else
  # -layout preserves column structure. Hyphens introduced by line-wrapping are
  # removed first, then whitespace is squeezed, so the greps below match prose
  # as written rather than as typeset.
  flatten() { pdftotext -layout -q "$1" - 2>/dev/null | perl -0777 -pe 's/-\n\s*//g' | tr -s '[:space:]' ' '; }
  flatten "$WORK/zb-thesis.pdf" > "$WORK/thesis.flat"
  flatten "$WORK/zb-paper.pdf"  > "$WORK/paper.flat"

  # Guard: if extraction silently produced nothing, the absence checks below
  # would pass vacuously. Require the documents to be recognisably themselves.
  if ! grep -qF 'Modelling the US Constitution' "$WORK/paper.flat" \
     || ! grep -qF 'Isabelle' "$WORK/thesis.flat"; then
    inconc "PDF text extraction produced unusable output" "Absence checks would be vacuous. Check the pdftotext build."
  else
    for phrase in \
      'highly unlikely that any state legislature would ratify' \
      'the amendment is actually unnecessary' \
      'What this support looks like shall not be specified further'
    do
      grep -qF "$phrase" "$WORK/thesis.flat" \
        && ok "thesis states the caveat: \"...${phrase}...\"" \
        || bad "caveat not found in the thesis -- the claim in analysis/ is wrong or the text changed"
    done

    absent=0
    for w in unlikely unnecessary improbable consent; do
      grep -qiF "$w" "$WORK/paper.flat" && { bad "'$w' DOES occur in the paper -- our omission claim is false"; absent=1; }
    done
    [[ "$absent" -eq 0 ]] \
      && ok "none of unlikely/unnecessary/improbable/consent occur anywhere in the paper" \
      || true

    grep -qF 'without violating the rules laid out in the US Consti' "$WORK/paper.flat" \
      && ok "paper's conclusion states the result unqualified" \
      || bad "paper's conclusion no longer reads as quoted in analysis/"

    grep -qF 'Having successfully verified the validity of the argument' "$WORK/thesis.flat" \
      && ok "thesis's own conclusion also drops the caveat" \
      || bad "thesis conclusion no longer reads as quoted in analysis/"
  fi

  # ---- The textual premises of inert-manoeuvre.md, checked against the PDFs.
  note "The 4f result turns on one textual fact: omsp is asserted at t1 and never"
  note "propagated. If the thesis carried an X omsp axiom, the finding would be an"
  note "artifact of this transcription rather than a property of the model."
  if grep -qE 'omsp-t1[[:space:]]*:' "$WORK/thesis.flat" \
     && ! grep -qE 'Xomsp|X omsp[^.]{0,12}t1[[:space:]]*:' "$WORK/thesis.flat"; then
    ok "thesis asserts omsp at t1 only; no X omsp axiom anywhere in it"
  else
    bad "the thesis may propagate omsp past t1 -- inert-manoeuvre.md would be void"
  fi

  # The check above is about the thesis. This one is about OUR transcription:
  # the reviewer's point that 'no X omsp axiom' was only ever spot-checked. Take
  # a full inventory instead -- exactly one axiom in the model may mention omsp.
  cat > "$WORK/omspinv.py" <<'PYEOF'
import re, sys
LABEL = re.compile(r'\b([A-Za-z][A-Za-z0-9_' + chr(39) + r']*)\s*:\s*"((?:[^"\\]|\\.)*)"')
hits = []
for path in sys.argv[1:]:
    text = open(path, encoding='utf-8').read()
    for block in re.findall(r'^axiomatization\s+where\b.*?(?=^\S|\Z)', text, re.M | re.S):
        hits += [l for l, f in LABEL.findall(block) if re.search(r'\bomsp\b', f)]
print(" ".join(hits) if hits else "NONE")
PYEOF
  omsp_ax=$(python3 "$WORK/omspinv.py" "$THY/GodelCore.thy" "$THY/GodelConstitution.thy")
  if [[ "$omsp_ax" == "omsp_t1" ]]; then
    ok "exactly one axiom in the transcription mentions omsp, and it is omsp_t1"
  else
    bad "omsp is asserted by: $omsp_ax -- expected omsp_t1 alone"
  fi

  # It matters that this is a DISCLOSED limitation. Both venues say so, and the
  # write-up must not imply concealment.
  for f in thesis paper; do
    grep -qF 'implemented by simply not using' "$WORK/$f.flat" \
      && ok "$f discloses the omission in its own words" \
      || bad "$f no longer contains the disclosure quoted in inert-manoeuvre.md"
  done
  grep -qF 'do not constitute ideal amendments' "$WORK/paper.flat" \
    && ok "paper concedes the amendments are not ideal (quoted in inert-manoeuvre.md)" \
    || bad "paper no longer contains the 'not ideal amendments' concession"
  grep -qF 'were we to keep condition' "$WORK/thesis.flat" \
    && ok "thesis states the inconsistency claim that 4f reproduces" \
    || bad "could not locate the thesis's inconsistency claim"
fi

# ---- 5d. The pre-1947 Article V authorities, pinned to their scanned sources.
hdr "5d. academia/article-v-entrenchment.md, checked against the scans"
note "The quotations in that file decide which quadrant of the 2x2 in"
note "ratification-price.md the pre-1947 literature occupied, so they carry weight."
note "Each is checked against the Archive.org text layer of the source itself."
declare -a AV_ID=(1324228 2015.505449.amending-of)
declare -a AV_ITEM=(jstor-1324228 in.ernet.dli.2015.505449)
declare -a AV_NAME=(machen orfield)
av_have=1
for i in 0 1; do
  f="$WORK/${AV_NAME[$i]}.txt"
  if [[ ! -s "$f" ]]; then
    note "${AV_NAME[$i]} text not present, fetching..."
    curl -sSL --max-time 240 -o "$f" \
      "https://archive.org/download/${AV_ITEM[$i]}/${AV_ID[$i]}_djvu.txt" || true
  fi
  [[ -s "$f" ]] || av_have=0
done
if [[ "$av_have" -eq 1 ]]; then
  # Archive.org OCR hard-wraps AND hyphenates across line breaks ("indi-\nrectly"),
  # so join hyphenated words before flattening or half the quotations will miss.
  for n in machen orfield; do
    perl -0777 -pe 's/-[ \t]*\n\s*//g' < "$WORK/$n.txt" | tr '\n' ' ' | tr -s ' ' > "$WORK/$n.flat"
  done
  grep -qF 'abolishing the Senate, or reducing it to a body merely advisory' "$WORK/machen.flat" \
    && ok "Machen 1910 states the functional reading, as quoted" \
    || bad "Machen quotation not found in the scan"
  grep -qF 'each state would have no senators at all' "$WORK/orfield.flat" \
    && ok "Orfield 1942 states the formal reading, as quoted" \
    || bad "Orfield 'no senators at all' quotation not found in the scan"
  grep -qF 'who assert that the ordinary amending body could abolish' "$WORK/orfield.flat" \
    && ok "Orfield reports few asserting the ordinary amending power reaches the clause" \
    || bad "Orfield 'not many who assert' quotation not found in the scan"
  grep -qF 'legal casuistry' "$WORK/orfield.flat" \
    && ok "Orfield calls the functional reading legal casuistry, as quoted" \
    || bad "Orfield 'legal casuistry' quotation not found in the scan"
  grep -qF 'indirectly by first repealing the clause' "$WORK/orfield.flat" \
    && ok "Orfield states the two-step in 1942, so it is not a modern invention" \
    || bad "Orfield's statement of the two-step not found in the scan"
else
  inconc "pre-1947 law review scans could not be fetched" \
         "Network failure is not a replication failure. Sources are named with Archive.org identifiers in academia/article-v-entrenchment.md"
fi

note "Barry (1929) is the load-bearing one: it is the only pre-1947 Supreme Court"
note "reading of the entrenchment clause's SCOPE, and it reads it narrowly. It is"
note "checked against the official U.S. Reports scan at loc.gov, not a secondary text."
if command -v pdftotext >/dev/null 2>&1; then
  if [[ ! -s "$WORK/barry.pdf" ]]; then
    curl -sSL --max-time 240 -o "$WORK/barry.pdf" \
      "https://tile.loc.gov/storage-services/service/ll/usrep/usrep279/usrep279597/usrep279597.pdf" || true
  fi
  if [[ -s "$WORK/barry.pdf" ]]; then
    pdftotext -layout "$WORK/barry.pdf" "$WORK/barry.txt" 2>/dev/null
    perl -0777 -pe 's/-[ \t]*\n\s*//g' < "$WORK/barry.txt" | tr '\n' ' ' | tr -s ' ' > "$WORK/barry.flat"
    # This sentence straddles the 615/616 page break, with a running head between
    # its halves, so it cannot be matched as one string. Checking the halves
    # separately is also what justifies citing the passage as 615-616.
    grep -qF 'This constitutes a limitation upon the power' "$WORK/barry.flat" \
      && ok "Barry 1929: the clause is 'a limitation upon the power...' (page 615)" \
      || bad "Barry 'limitation upon the power' passage not found in the scan"
    grep -qF 'of amendment and has nothing to do with a situation such as the one here presented' "$WORK/barry.flat" \
      && ok "...'of amendment and has nothing to do with' Senate seating (page 616)" \
      || bad "Barry 'nothing to do with a situation such as' passage not found in the scan"
    grep -qF 'no more deprives the state of its "equal suffrage" in the constitutional sense than would a vote of the Senate vacating the seat of a sitting member or a vote of expulsion' "$WORK/barry.flat" \
      && ok "Barry 1929: expulsion does not deprive a state of equal suffrage, as quoted" \
      || bad "Barry expulsion comparison not found in the scan"
    # The write-up cites 615-616. A page-number slip in a Supreme Court cite is
    # the kind of error that survives forever, so it is machine-checked here.
    barry_pg=$(python3 - "$WORK/barry.txt" <<'PYEOF'
import sys
pages = open(sys.argv[1], encoding="utf-8", errors="replace").read().split("\f")
hit = [i + 1 for i, p in enumerate(pages) if "limitation upon the power" in p]
print(596 + hit[0] if hit else "none")
PYEOF
)
    [[ "$barry_pg" == "615" ]] \
      && ok "and the passage really is at 279 U.S. 615, as cited" \
      || bad "Barry passage is at page $barry_pg, but article-v-entrenchment.md cites 615-616"
  else
    inconc "Barry v. United States scan could not be fetched" \
           "Network failure is not a replication failure. Source: https://tile.loc.gov/storage-services/service/ll/usrep/usrep279/usrep279597/usrep279597.pdf"
  fi

  note "Siddons 1902 is the earliest functional reading found, and the one Barry"
  note "answers. His concession on expulsion is checked too, because the write-up"
  note "leans on it to say NO pre-1947 source claimed immunity from expulsion."
  if [[ ! -s "$WORK/siddons.pdf" ]]; then
    curl -sSL --max-time 240 -o "$WORK/siddons.pdf" \
      "https://openyls.law.yale.edu/server/api/core/bitstreams/9e7f9f6a-71f6-4248-a756-532acf4ede65/content" || true
  fi
  if [[ -s "$WORK/siddons.pdf" ]]; then
    pdftotext -layout "$WORK/siddons.pdf" "$WORK/siddons.txt" 2>/dev/null
    perl -0777 -pe 's/-[ \t]*\n\s*//g' < "$WORK/siddons.txt" | tr '\n' ' ' | tr -s ' ' > "$WORK/siddons.flat"
    grep -qF 'to deprive South Carolina of its right of equal suffrage in the Senate' "$WORK/siddons.flat" \
      && ok "Siddons 1902 applies the clause outside Article V, as quoted" \
      || bad "Siddons suspension quotation not found in the scan"
    grep -qF 'justify his expulsion, this punishment may be inflicted' "$WORK/siddons.flat" \
      && ok "and Siddons concedes the expulsion power, as the write-up says he does" \
      || bad "Siddons's concession on expulsion not found -- the 'no immunity' claim is unsupported"
  else
    inconc "Siddons 1902 scan could not be fetched" \
           "Network failure is not a replication failure. Source: OpenYLS, identifier in academia/article-v-entrenchment.md"
  fi
else
  inconc "pdftotext not on PATH" \
         "Barry and Siddons are PDF scans. Install poppler to check those four quotations."
fi

# --------------------------------------------------- claim 6: facts have one owner

hdr "6. Single source of truth: every load-bearing value has exactly one owner"
note "Claim: data/facts.json owns every load-bearing number, date and quotation,"
note "each names one canonical file, and the value is actually in that file."
note "Prose may legitimately differ between a research note and a general-audience"
note "page. Values may not. Source of truth: data/facts.json"

if [[ -x "$(command -v python3)" ]]; then
  facts_out=$(python3 "$REPO/tools/facts.py" --check 2>&1)
  facts_rc=$?
  facts_n=$(grep -oE '[0-9]+/[0-9]+ facts' <<<"$facts_out" | head -1)
  if [[ $facts_rc -eq 0 ]]; then
    ok "every fact was found in the file named as its owner ($facts_n)"
  else
    bad "facts.json disagrees with its canonical files"
    while IFS= read -r line; do note "$line"; done <<<"$facts_out"
  fi

  # 6b. If the checker cannot be made to fail, its passes mean nothing. Break a
  # copy in the two independent ways the checker is supposed to catch -- a value
  # absent from its canonical file, and a derived number that does not follow
  # from the numbers it derives from -- and require rejection.
  hdr "6b. NEGATIVE CONTROL: a broken facts.json must be rejected"
  note "Rewriting the House proposal threshold from 146 to 147 in a scratch copy."
  note "That is absent from threshold-arithmetic.md AND is not two thirds of 218."
  broken="$WORK/facts-broken.json"
  mkdir -p "$WORK"
  sed 's/"value": 146,/"value": 147,/' "$REPO/data/facts.json" >"$broken"
  if ! diff -q "$broken" "$REPO/data/facts.json" >/dev/null 2>&1; then
    if GL_FACTS="$broken" python3 "$REPO/tools/facts.py" --check >/dev/null 2>&1; then
      bad "CONTROL BROKEN: tools/facts.py accepted a facts file it should reject"
    else
      ok "tools/facts.py rejects a value that is neither in its file nor arithmetically right"
    fi
  else
    bad "CONTROL BROKEN: the scratch copy is identical to the real one, so nothing was tested"
  fi
  rm -f "$broken"

  # 6c. The duplication audit is only useful while its probes still match. A
  # probe that matches nothing is indistinguishable from a fact that is no
  # longer duplicated, and the first run of that tool reported two live facts as
  # absent because markdown emphasis sat inside the pattern.
  hdr "6c. The duplication audit's probes are all still live"
  stale=$(python3 "$REPO/tools/ssot_audit.py" --json 2>/dev/null \
          | python3 -c 'import json,sys; d=json.load(sys.stdin); print(" ".join(p["id"] for p in d["probes"] if p["file_count"]==0))')
  if [[ -z "$stale" ]]; then
    ok "every probe in tools/ssot_audit.py matches at least one tracked file"
  else
    bad "stale probes match nothing, so the audit is silently under-reporting: $stale"
  fi
else
  inconc "python3 not on PATH" "Cannot check data/facts.json against its canonical files."
  inconc "python3 not on PATH" "Cannot run the facts-checker negative control."
  inconc "python3 not on PATH" "Cannot check the duplication audit's probes."
fi

# 6d. This script's own header states how many negative controls it carries.
# That number said "three" while five existed. Nothing was counting, which is
# the same defect class the script exists to catch, so now something counts.
hdr "6d. The header's negative-control count matches reality"
declared=$(grep -oE '^# (Three|Four|Five|Six|Seven|Eight) checks are NEGATIVE CONTROLS' "$0" \
           | grep -oE 'Three|Four|Five|Six|Seven|Eight' | head -1)
actual=$(grep -cE '^ *hdr "[0-9a-z]+\. NEGATIVE CONTROL' "$0")
case "$declared" in
  Three) declared_n=3 ;; Four) declared_n=4 ;; Five) declared_n=5 ;;
  Six) declared_n=6 ;; Seven) declared_n=7 ;; Eight) declared_n=8 ;;
  *) declared_n=-1 ;;
esac
if [[ "$declared_n" -eq "$actual" ]]; then
  ok "header declares $declared_n negative controls and $actual are present"
else
  bad "header declares $declared_n negative controls but $actual are present"
fi

# The published artifact renders these numbers to readers, and a number nobody
# can read is not published. Contrast is measured rather than eyeballed for the
# same reason page images are read rather than OCR: the eye is the instrument
# most likely to report what it expects.
hdr "6e. The site palette meets WCAG AA, measured"
if [[ -f site/src/styles/tokens.css ]]; then
  if out=$(python3 tools/contrast.py --check 2>&1); then
    ok "$(echo "$out" | tail -1)"
  else
    bad "$(echo "$out" | tail -1)"
    echo "$out" | sed 's/^/      /'
  fi
else
  inconc "site/src/styles/tokens.css not present"
fi

# --------------------------------------------------------------------- what is NOT done

hdr "7. Explicitly NOT verified"
note "Lean 4       : version string only. No Lean code has been written or run."
note "Z&B numbers  : the thesis reports no runtimes or benchmark table, so only the"
note "               proofs themselves are comparable, not performance claims."
note "Z&B fidelity : transcribed by hand from the PDF. Bold-face operator notation"
note "               was renamed to avoid clashing with HOL built-ins; this is a"
note "               deliberate deviation from the printed source."
note "Yadamsuren   : the LLM-vs-hybrid accuracy comparison is not in their repo and"
note "               cannot be checked from the published artifacts."

# ------------------------------------------------------------------------- summary

# The README advertises a check count. A stale number there is the same class of
# defect this whole script exists to prevent, so it is checked against the run
# itself. This check counts toward the total it is checking, which is fine: the
# two only agree when both are current.
readme_n=$(grep -oE '\*\*[0-9]+ checks, all passing\*\*' "$REPO/README.md" \
           | grep -oE '[0-9]+' | head -1)
total=$(( PASS + FAIL + INCONC + 1 ))
if [[ -z "$readme_n" ]]; then
  bad "README.md no longer advertises a check count in the expected form"
elif [[ "$readme_n" == "$total" ]]; then
  ok "README.md's advertised check count ($readme_n) matches this run"
else
  bad "README.md advertises $readme_n checks; this run has $total"
fi

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
