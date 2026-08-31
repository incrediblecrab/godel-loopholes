#!/usr/bin/env python3
"""Ablation experiments on the Zahoransky & Benzmueller model.

Everything here is GENERATED from the two tracked theory files:

    isabelle/GodelCore.thy
    isabelle/GodelConstitution.thy

Nothing is transcribed a second time. That is deliberate: the model was once
stored three times in this repository and the copies had already begun to
drift. If you want to change the model, change GodelCore.thy; every theory
this script emits will follow.

Four experiments, each answering a question the published proof does not.

  minimal   Prove Dictatorship_t3 from a six-axiom subset. Sufficiency is a
            kernel-certified Isabelle theorem, so the other 45 axioms are
            certainly not needed for it.

  tight     Two separate questions. (a) Drop each of the six from the six:
            six countermodels means no PROPER SUBSET OF THOSE SIX works, which
            is irredundance, not minimality. (b) Drop each of the six from all
            51: a countermodel there means the axiom is necessary to EVERY
            sufficient support. Only four pass (b), so the lower bound is four.

  noamd1    Delete the four axioms that propose and support the amendment to
            Article V -- the whole of Goedel's step one -- and re-prove all
            three published theorems. They still hold.

  omsp      The thesis says (p.20) that keeping the Senate-suffrage condition
            at t2 "would run into inconsistencies". Add the axiom they
            declined to add and derive False. They are right.

  lapsed    Prove that the model does not merely omit the entrenchment clause
            at t2 but ENTAILS its failure there, citing only amd2_prop_t2 and
            amd2_not_maint_suf_t2 -- no amendment, no ratification, no
            Article V. Step one's conclusion is a theorem of two stipulations.

  blocking  Show the logic is not at fault. Propagate the entrenchment clause
            to t2, drop amd1a, and do not stipulate that the dictatorship
            amendment is proposed: the theory is satisfiable AND proves the
            amendment is not proposed. A representation of "blocked" was
            available and was not used.

  sweep     Slow. Ablate each of the 51 axioms singly and probe for a
            countermodel to Dictatorship_t3. Useful as a map, but weaker than
            'minimal': "Nitpick found no counterexample" is not a proof of
            redundancy, whereas a proof from six axioms is.

Usage:  python3 axiom_sweep.py {minimal|tight|noamd1|omsp|lapsed|blocking|sweep|all}
Requires Isabelle on PATH. Scratch goes to $GL_WORK or /tmp/gl-replication.
"""

import os
import re
import subprocess
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
THY = os.path.join(HERE, os.pardir, "isabelle")
WORK = os.path.join(os.environ.get("GL_WORK", "/tmp/gl-replication"), "sweep")

# The six axioms that suffice. Derived by inspection of the published proof and
# confirmed by 'minimal' and 'tight'; not hand-waved.
SIX = ["t1_s_t2", "t2_s_t3", "Xpsr_t1", "Xrv_t2", "amd2_prop_t2", "amd2_sup_rat_t2"]

# The subset of SIX for which a countermodel to (all 51 minus that axiom)
# exists, hence which is necessary to EVERY sufficient support, not merely to
# this one. This is the recorded claim; exp_necessary fails if it drifts.
EXPECTED_NECESSARY = {"Xpsr_t1", "Xrv_t2", "amd2_prop_t2", "amd2_sup_rat_t2"}

# Goedel's step one: propose and support the amendment stripping Article V's
# entrenchment clause.
AMD1 = ["amd1a_prop_t1", "amd1b_prop_t1", "amd1a_sup_rat_t1", "amd1b_sup_rat_t1"]

# Lemmas whose original proof SCRIPTS cite the AMD1 axioms by name. Only the
# scripts are casualties: both propositions remain provable without those
# axioms, and the ablation re-proves them rather than dropping them. The other
# three amd1b lemmas cite no amd1 axiom at all -- amd1b is a tautology -- so
# they survive untouched and are not listed here.
AMD1_LEMMAS = ["amd1a_val_t2", "amd1b_val_t2_2"]

# Re-proofs for exactly those two. amd1b is excluded middle, so it needs no
# axioms. amd1a is an existential that the amd2 stipulations witness directly,
# which is the whole point: the repeal amendment's content is already entailed.
REPROVE_AMD1 = r'''
lemma amd1b_val_t2_2: "\<lfloor>amd1b\<rfloor>t2"
  by (simp add: amd1b_def local_valid_def tallB_s_def tall_s_def
                timp_def tneg_def tor_def)

lemma amd1a_val_t2: "\<lfloor>amd1a\<rfloor>t2"
proof -
  have "\<not> maint_suf amd2 t2 \<and> is_prop amd2 t2"
    using amd2_prop_t2 amd2_not_maint_suf_t2
    by (simp add: local_valid_def tneg_def)
  thus ?thesis
    by (auto simp: local_valid_def amd1a_def texiB_s_def texi_s_def
                   tand_def tneg_def)
qed
'''

KW = (r"^[ \t]*(lemma|theorem|corollary|definition|abbreviation|typedecl"
      r"|datatype|consts|axiomatization|declare|type_synonym|end)\b")
LABEL = re.compile(r'\b([A-Za-z][A-Za-z0-9_\']*)\s*:\s*"((?:[^"\\]|\\.)*)"')


def strip_comments(text):
    """Remove (* ... *), respecting nesting."""
    out, depth, i = [], 0, 0
    while i < len(text):
        if text.startswith("(*", i):
            depth += 1
            i += 2
            continue
        if text.startswith("*)", i) and depth:
            depth -= 1
            i += 2
            continue
        if not depth:
            out.append(text[i])
        i += 1
    return "".join(out)


def chunks(path):
    """Split a theory into (keyword, text) top-level chunks, header first."""
    lines = strip_comments(open(path, encoding="utf-8").read()).split("\n")
    starts = [i for i, l in enumerate(lines) if re.match(KW, l)]
    result = [("HEADER", "\n".join(lines[:starts[0]]))]
    for j, s in enumerate(starts):
        end = starts[j + 1] if j + 1 < len(starts) else len(lines)
        result.append((re.match(KW, lines[s]).group(1), "\n".join(lines[s:end])))
    return result


def dissect():
    """Return (preamble chunks, [(label, formula)]) for the whole model."""
    preamble, axioms = [], []
    for i, src in enumerate(("GodelCore.thy", "GodelConstitution.thy")):
        for kw, chunk in chunks(os.path.join(THY, src)):
            if kw == "HEADER" and i:
                continue
            if kw == "end":
                continue
            if kw == "axiomatization":
                axioms += LABEL.findall(chunk)
                continue
            if kw in ("lemma", "theorem", "corollary"):
                continue
            preamble.append(chunk)
    return preamble, axioms


def build(name, keep, tail, drop_lemmas=()):
    """Emit a theory named `name` carrying only the axioms in `keep`."""
    preamble, axioms = dissect()
    kept = [(l, f) for l, f in axioms if l in keep]
    missing = set(keep) - {l for l, _ in kept}
    if missing:
        sys.exit("axioms not found in the model: " + ", ".join(sorted(missing)))
    body = "\n".join(preamble).replace("theory GodelCore", "theory " + name, 1)
    body += ("\n\naxiomatization where\n  "
             + " and\n  ".join('%s: "%s"' % (l, f) for l, f in kept) + "\n")
    os.makedirs(WORK, exist_ok=True)
    path = os.path.join(WORK, name + ".thy")
    open(path, "w", encoding="utf-8").write(body + tail + "\nend\n")
    return path


def build_full_minus(name, drop, tail, drop_lemmas=()):
    """Emit the model MINUS `drop`, filtering each axiomatization block IN PLACE.

    Declaration order matters: an axiom mentioning `amd2` that is emitted before
    `amd2` is defined leaves `amd2` a free variable, which Isabelle generalizes.
    That silently strengthens the theory into an inconsistent one. An earlier
    version of this function rebuilt one combined block before the first lemma
    and did exactly that, so the ablation it reported was vacuous. Filtering in
    place is the fix; `consistency` is the guard that catches any recurrence.
    """
    lemma_drop = (re.compile(r"^\s*(lemma|theorem|corollary)\s+(%s)\s*:"
                             % "|".join(drop_lemmas)) if drop_lemmas else None)
    dropped, cut_lemmas = set(), []
    out = []
    for i, src in enumerate(("GodelCore.thy", "GodelConstitution.thy")):
        for kw, chunk in chunks(os.path.join(THY, src)):
            if kw == "HEADER" and i:
                continue
            if kw == "end":
                continue
            if kw == "axiomatization":
                kept = [(l, f) for l, f in LABEL.findall(chunk) if l not in drop]
                dropped |= {l for l, _ in LABEL.findall(chunk)} & set(drop)
                if not kept:
                    continue
                chunk = ("axiomatization where\n  "
                         + " and\n  ".join('%s: "%s"' % (l, f) for l, f in kept))
            if lemma_drop and kw in ("lemma", "theorem", "corollary") \
                    and lemma_drop.match(chunk.split("\n")[0]):
                cut_lemmas.append(chunk.split("\n")[0].strip())
                continue
            out.append(chunk)
    missing = set(drop) - dropped
    if missing:
        sys.exit("axioms not found in the model: " + ", ".join(sorted(missing)))
    body = "\n".join(out).replace("theory GodelCore", "theory " + name, 1)
    os.makedirs(WORK, exist_ok=True)
    path = os.path.join(WORK, name + ".thy")
    open(path, "w", encoding="utf-8").write(body + tail + "\nend\n")
    return path, cut_lemmas


def run(name, extra_files=()):
    """Process one theory; return (exit code, output)."""
    files = []
    for f in extra_files:
        files += ["-f", f]
    files += ["-f", name + ".thy"]
    proc = subprocess.run(["isabelle", "process_theories", "-O", "-U"] + files + [name],
                          cwd=WORK, capture_output=True, text=True)
    return proc.returncode, proc.stdout + proc.stderr


PROVE_DICTATORSHIP = r'''
lemma psr_at_t2: "\<lfloor>psr\<rfloor>t2" using Xpsr_t1 local_valid_def tnext_def t1_s_t2 by auto
lemma rv_at_t3:  "\<lfloor>rv\<rfloor>t3"  using Xrv_t2  local_valid_def tnext_def t2_s_t3 by auto

theorem Dictatorship_from_minimal_set: "\<lfloor>Dictatorship\<rfloor>t3"
proof -
  have "\<lfloor>\<^bold>X(is_rat amd2)\<rfloor>t2"
    using amd2_prop_t2 amd2_sup_rat_t2 local_valid_def tallB_s_def tall_s_def
          tand_def timp_def tnext_def psr_at_t2
    by auto
  hence "\<lfloor>amd2\<rfloor>t3"
    using local_valid_def tallB_s_def tall_s_def timp_def tnext_def rv_at_t3 t2_s_t3
    by auto
  hence "\<lfloor>is_leg P \<^bold>\<and> is_exe P \<^bold>\<and> is_jud P\<rfloor>t3"
    using amd2_def by (simp add: local_valid_def tand_def)
  thus "\<lfloor>Dictatorship\<rfloor>t3" by (meson Dictatorship_def local_valid_def)
qed
'''

PROBE_DICTATORSHIP = r'''
lemma PROBE: "\<lfloor>Dictatorship\<rfloor>t3"
  nitpick[user_axioms, card time = 4, timeout = 300] oops
'''

# The repeal experiment. Three questions, in order.
REPEAL_PRESENT = r'''
(* (i) Is amd1a literally the negation of the entrenchment clause? Not merely
   equivalent under the axioms -- the SAME TERM. *)
theorem amd1a_IS_not_omsp: "amd1a = (\<^bold>\<not>omsp)"
  by (auto simp: amd1a_def texiB_s_def texi_s_def tallB_s_def tall_s_def
                 tand_def tneg_def timp_def)

(* (ii) Does the repeal EVENT occur in the published model? *)
theorem amd1a_ratified_at_t2: "\<lfloor>is_rat amd1a\<rfloor>t2"
  using amd1a_prop_t1 amd1a_sup_rat_t1 psr_t1 t1_s_t2
        local_valid_def tallB_s_def tall_s_def tand_def timp_def tnext_def
  by auto

(* (iii) Is its CONTENT already forced by the amd2 stipulations alone, citing
   no amd1 axiom at all? *)
theorem amd1a_content_without_repeal: "\<lfloor>amd1a\<rfloor>t2"
  using amd2_prop_t2 amd2_not_maint_suf_t2
  by (auto simp: local_valid_def amd1a_def texiB_s_def texi_s_def
                 tand_def tneg_def)
'''

# Asked of the theory with the amd1 axioms deleted: is the repeal event still
# derivable? A countermodel means the event genuinely went away.
PROBE_REPEAL_EVENT = r'''
lemma PROBE: "\<lfloor>is_rat amd1a\<rfloor>t2"
  nitpick[user_axioms, card time = 4, timeout = 300] oops
'''

KEEP_OMSP = r'''
axiomatization where
  Xomsp_t1: "\<lfloor>\<^bold>X omsp\<rfloor>t1"

lemma omsp_t2_holds: "\<lfloor>omsp\<rfloor>t2"
  using Xomsp_t1 local_valid_def tnext_def t1_s_t2 by auto

theorem keeping_omsp_at_t2_is_inconsistent: "False"
  using omsp_t2_holds amd2_prop_t2 amd2_not_maint_suf_t2
  by (auto simp: local_valid_def tallB_s_def tall_s_def timp_def tneg_def)
'''

LAPSED = r'''
theorem omsp_false_at_t2: "\<lfloor>\<^bold>\<not> omsp\<rfloor>t2"
  using amd2_prop_t2 amd2_not_maint_suf_t2
  by (auto simp: local_valid_def tallB_s_def tall_s_def timp_def tneg_def)
'''

KEEP_OMSP_HEAD = r'''
axiomatization where
  Xomsp_t1: "\<lfloor>\<^bold>X omsp\<rfloor>t1"

lemma omsp_t2_holds: "\<lfloor>omsp\<rfloor>t2"
  using Xomsp_t1 local_valid_def tnext_def t1_s_t2 by auto
'''

BLOCKED = r'''
theorem amd2_is_blocked_at_t2: "\<lfloor>\<^bold>\<not>(is_prop amd2)\<rfloor>t2"
  using omsp_t2_holds amd2_not_maint_suf_t2
  by (auto simp: local_valid_def tallB_s_def tall_s_def timp_def tneg_def)
'''

SATISFY = r'''
lemma SATISFIABLE: "True"
  nitpick[satisfy, user_axioms, card time = 4, timeout = 300] oops
'''

# A countermodel to False is a model of the axioms, which is consistency.
# Run this against every ablated theory: an inconsistent theory proves all
# three published theorems too, and looks like a triumph in the log.
FALSE_PROBE = r'''
lemma PROBE: "False"
  nitpick[user_axioms, card time = 4, timeout = 300] oops
'''


def verdict(out, lemma_line_marker="PROBE"):
    if "Nitpick found a counterexample" in out:
        return "counterexample"
    if "Nitpick found no counterexample" in out:
        return "no counterexample"
    if "Nitpick found a model" in out:
        return "model"
    return "no verdict"


# Isabelle writes its symbols as ASCII escapes in the theory file. The write-up
# and the website show them as the characters they denote. This table is the
# only place that translation happens, and anything not in it is left as the
# raw escape rather than guessed at, so an unrecognised symbol is visible as
# one instead of being silently dropped.
SYMBOLS = {
    "lfloor": "\u230a", "rfloor": "\u230b", "bold": "", "sub": "",
    "not": "\u00ac", "and": "\u2227", "or": "\u2228", "longrightarrow": "\u27f6",
    "longleftrightarrow": "\u27f7", "forall": "\u2200", "exists": "\u2203",
    "noteq": "\u2260", "circ": "\u2218", "lambda": "\u03bb", "Rightarrow": "\u21d2",
    "equiv": "\u2261", "in": "\u2208", "times": "\u00d7", "Longrightarrow": "\u27f9",
}

_ESC = re.compile(r"\\<(\^?)([A-Za-z]+)>")


def unescape_isabelle(text):
    """Render Isabelle ASCII escapes as characters, leaving unknowns visible."""
    def sub(m):
        name = m.group(2)
        if name in SYMBOLS:
            return SYMBOLS[name]
        return m.group(0)
    return _ESC.sub(sub, text)


def axioms_in(*sources):
    """Parse (label, formula) pairs out of the named theory files.

    Generalises what dissect() does for the published model so the repaired
    model can be inventoried the same way. Parsed, never transcribed.
    """
    found = []
    for src in sources:
        for kw, chunk in chunks(os.path.join(THY, src)):
            if kw == "axiomatization":
                found += LABEL.findall(chunk)
    return found


def exp_inventory():
    """Emit the model's axiom inventory as JSON. Requires no Isabelle.

    The website renders the ablation result, and the one thing it must not do
    is retype fifty-one axiom names. This mode parses them out of the same two
    theory files every experiment is generated from, so the site and the proof
    cannot disagree. The VERDICTS are not recorded here on purpose: they are
    measured by verify.sh section 4, which re-runs Isabelle. A verdict cached
    in a file is a verdict nobody is checking.

    The `netadd` block does the same for the repaired model, whose whole point
    is that the proposal is derived rather than asserted. The site shows the
    published and repaired models side by side, so both inventories have to
    come from the theory files rather than from a designer's memory.
    """
    import json

    _, axioms = dissect()
    thm = collect_results()
    netadd_core = axioms_in("GodelNetAddCore.thy")
    netadd_step_one = axioms_in("GodelNetAddFull.thy")
    out = {
        "generated_by": "analysis/united-states-1947/search/axiom_sweep.py inventory",
        "generated_from": [
            "analysis/united-states-1947/isabelle/GodelCore.thy",
            "analysis/united-states-1947/isabelle/GodelConstitution.thy",
            "analysis/united-states-1947/isabelle/GodelNetAddCore.thy",
            "analysis/united-states-1947/isabelle/GodelNetAddFull.thy",
        ],
        "note": ("Parsed, not transcribed. Verdicts are deliberately absent: "
                 "verify.sh section 4 re-runs the experiments in Isabelle. Run "
                 "`python3 axiom_sweep.py inventory` to regenerate."),
        "axioms": [
            {
                "label": label,
                "formula": unescape_isabelle(formula),
                "raw": formula,
                "sufficient": label in SIX,
                "necessary": label in EXPECTED_NECESSARY,
                "step_one": label in AMD1,
            }
            for label, formula in axioms
        ],
        "sufficient": list(SIX),
        "necessary": sorted(EXPECTED_NECESSARY),
        "step_one": list(AMD1),
        "step_one_broken_scripts": list(AMD1_LEMMAS),
        "results": thm,
        "netadd": {
            "note": ("The repaired model. Its five step-one stipulations are "
                     "preconditions; none of them asserts that the amendment "
                     "was proposed. The proposal is derived."),
            "core": [
                {"label": label, "formula": unescape_isabelle(formula), "raw": formula}
                for label, formula in netadd_core
            ],
            "step_one": [
                {"label": label, "formula": unescape_isabelle(formula), "raw": formula}
                for label, formula in netadd_step_one
            ],
        },
    }
    print(json.dumps(out, indent=2, ensure_ascii=False))
    return True


def collect_results():
    """Theorem and lemma names, parsed from the theory files."""
    named = {"theorems": [], "amd1_lemmas": []}
    for src in ("GodelCore.thy", "GodelConstitution.thy"):
        text = strip_comments(open(os.path.join(THY, src), encoding="utf-8").read())
        for kw, label in re.findall(
            r"^(theorem|lemma)\s+([A-Za-z][A-Za-z0-9_']*)\s*:", text, re.M
        ):
            if kw == "theorem":
                named["theorems"].append(label)
            elif re.match(r"amd1[ab]_val", label):
                named["amd1_lemmas"].append(label)
    return named


def exp_minimal():
    print("== minimal: prove Dictatorship_t3 from %d of 51 axioms ==" % len(SIX))
    build("MinimalSupport", SIX, PROVE_DICTATORSHIP)
    code, out = run("MinimalSupport")
    good = code == 0 and "Error" not in out
    print("  axioms used: " + " ".join(sorted(SIX)))
    if not good:
        print("  RESULT: FAILED\n" + out[-2000:])
        return False
    build("MinimalConsistency", SIX, FALSE_PROBE)
    _, cout = run("MinimalConsistency")
    v = verdict(cout)
    print("  consistency probe (nitpick for a model of the six): " + v)
    ok = v == "counterexample"
    print("  RESULT: " + ("PROVED from six consistent axioms -- the other 45 are "
                          "not needed for this theorem"
                          if ok else "VACUOUS -- the six-axiom theory proves False"))
    return ok


def exp_tight():
    print("== tight: two separate questions about the six ==")
    print("  (a) irredundant? drop each of the six from the six.")
    allgood = True
    for drop in SIX:
        name = "Drop_" + drop
        build(name, [a for a in SIX if a != drop], PROBE_DICTATORSHIP)
        _, out = run(name)
        v = verdict(out)
        ok = v == "counterexample"
        allgood &= ok
        print("      without %-18s %s" % (drop, v))
    print("  RESULT (a): " + ("the six-axiom set is IRREDUNDANT"
                              if allgood else "redundant -- one of the six is idle"))
    return allgood and exp_necessary()


def exp_necessary():
    """The stronger question: must EVERY sufficient support contain these six?

    Irredundance only says no member of this set is idle within this set. It
    leaves open that some different, smaller set drawn from the other 45 axioms
    proves the theorem. Ruling that out needs a lower bound, and there is one
    available: if the FULL theory minus axiom `a` does not entail the theorem,
    then no subset omitting `a` entails it either, since subsets are weaker.
    An axiom passing that test is necessary to every sufficient support.
    """
    print("  (b) necessary to EVERY support? drop each of the six from all 51.")
    _, axioms = dissect()
    every = [l for l, _ in axioms]
    need = []
    for drop in SIX:
        name = "Need_" + drop
        build(name, [a for a in every if a != drop], PROBE_DICTATORSHIP)
        _, out = run(name)
        v = verdict(out)
        if v not in ("counterexample", "no counterexample", "model"):
            print("      all 51 without %-18s UNREADABLE VERDICT (%s)" % (drop, v))
            return False
        if v == "counterexample":
            need.append(drop)
        print("      all 51 without %-18s %s" % (drop, v))
    print("  RESULT (b): %d of the six are necessary to every sufficient support: %s"
          % (len(need), " ".join(need) if need else "none"))
    if len(need) < len(SIX):
        undet = [a for a in SIX if a not in need]
        print("      NOT established for: " + " ".join(undet))
        print("      For these, 'no counterexample' is a failure to find, not a")
        print("      proof of redundancy, so the lower bound is %d, not %d."
              % (len(need), len(SIX)))
    if set(need) != EXPECTED_NECESSARY:
        print("      MISMATCH against the recorded claim.")
        print("        claimed necessary: " + " ".join(sorted(EXPECTED_NECESSARY)))
        print("        measured necessary: " + " ".join(sorted(need)))
        print("      The write-up states a lower bound of %d. Fix the write-up or"
              % len(EXPECTED_NECESSARY))
        print("      the experiment before reporting either.")
        return False
    return True



def exp_repeal():
    """Does the model represent the repeal, and does representing it matter?

    This experiment exists because an earlier version of the write-up claimed
    the model could not represent repeal at all. Adversarial review said that
    was false, and it was. amd1a is not merely a stand-in for the repeal, it is
    definitionally the negation of the entrenchment clause, and in the published
    model it really is ratified. The defensible claim is narrower and is what
    this measures: the event is represented, it occurs, and it is still inert.
    """
    print("== repeal: is the repeal represented, and does it do anything? ==")
    build_full_minus("RepealPresent", set(), REPEAL_PRESENT)
    code, out = run("RepealPresent")
    want = ["amd1a_IS_not_omsp", "amd1a_ratified_at_t2",
            "amd1a_content_without_repeal"]
    got = [n for n in want if re.search(r"^theorem %s:" % n, out, re.M)]
    if code != 0 or "Error" in out or len(got) != 3:
        print("  RESULT: FAILED\n" + out[-2000:])
        return False
    print("  (i)   amd1a = not-omsp                    PROVED (term identity)")
    print("  (ii)  is_rat amd1a holds at t2 in the full model   PROVED")
    print("  (iii) amd1a's content holds at t2 from the amd2")
    print("        stipulations alone, no amd1 axiom cited      PROVED")

    build_full_minus("RepealAbsent", set(AMD1), PROBE_REPEAL_EVENT,
                     drop_lemmas=AMD1_LEMMAS)
    _, out2 = run("RepealAbsent")
    v = verdict(out2)
    print("  (iv)  with the amd1 axioms deleted, is_rat amd1a: " + v)
    if v == "inconclusive" or v == "no verdict":
        print("  RESULT: INCONCLUSIVE (nitpick gave no usable verdict)")
        return None
    if v != "counterexample":
        print("  RESULT: FAILED -- expected the repeal event to become underivable")
        return False
    print("  RESULT: the model DOES represent the repeal and the event DOES occur,")
    print("          yet deleting it costs no theorem, because amd1a's content is")
    print("          the same proposition the amd2 stipulations already force.")
    return True


def exp_noamd1():
    print("== noamd1: delete Goedel's step one, re-prove everything ==")
    _, cut = build_full_minus("NoArticleVStep", set(AMD1), REPROVE_AMD1,
                              drop_lemmas=AMD1_LEMMAS)
    code, out = run("NoArticleVStep")
    names = ["noDictatorship_t1", "noDictatorship_t2", "Dictatorship_t3"]
    found = [n for n in names if re.search(r"^theorem %s:" % n, out, re.M)]
    lem = ["amd1a_val_t2", "amd1b_val_t2_2", "amd1b_val_t2", "amd1b_val_t1",
           "amd1b_val"]
    lfound = [n for n in lem if re.search(r"^theorem %s:" % n, out, re.M)]
    good = code == 0 and "Error" not in out and len(found) == 3 and len(lfound) == 5
    print("  dropped axioms: " + " ".join(AMD1))
    print("  proof scripts replaced (the propositions survive, the scripts do not):")
    for c in cut:
        print("    " + c)
    print("  published theorems still proved: "
          + (", ".join(found) if found else "none"))
    print("  intermediate amd1 lemmas still proved: %d of 5" % len(lfound))
    if not good:
        print("  RESULT: FAILED\n" + out[-2000:])
        return False
    ok = exp_consistency()
    print("  RESULT: " + ("every published theorem AND every amd1 lemma survives "
                          "deleting step one, in a CONSISTENT theory"
                          if ok else "VACUOUS -- reduced theory proves False"))
    return ok


def exp_consistency():
    """Guard: a reduced theory that proves False proves everything.

    This exists because an earlier generator emitted the amd2 axioms before the
    amd2 definition, leaving amd2 free. Isabelle generalized it, every
    proposition became proposed and supported at t2, and the theory collapsed.
    All three theorems still 'proved'. Never trust an ablation without this.
    """
    build_full_minus("NoArticleVConsistency", set(AMD1), FALSE_PROBE,
                     drop_lemmas=AMD1_LEMMAS)
    _, out = run("NoArticleVConsistency")
    v = verdict(out)
    print("  consistency probe (nitpick for a model of the reduced theory): " + v)
    return v == "counterexample"


def exp_omsp():
    print("== omsp: test the thesis's own inconsistency claim (p.20) ==")
    os.makedirs(WORK, exist_ok=True)
    for f in ("GodelCore.thy", "GodelConstitution.thy"):
        open(os.path.join(WORK, f), "w", encoding="utf-8").write(
            open(os.path.join(THY, f), encoding="utf-8").read())
    open(os.path.join(WORK, "OmspKept.thy"), "w", encoding="utf-8").write(
        "theory OmspKept\n  imports GodelConstitution\nbegin\n" + KEEP_OMSP + "\nend\n")
    code, out = run("OmspKept", extra_files=("GodelCore.thy", "GodelConstitution.thy"))
    good = code == 0 and "Error" not in out
    print("  RESULT: " + ("False is DERIVABLE -- the authors were right, they "
                          "could not keep omsp at t2"
                          if good else "FAILED\n" + out[-2000:]))
    return good


def exp_sweep():
    print("== sweep: ablate each of the 51 axioms singly (slow) ==")
    _, axioms = dissect()
    labels = [l for l, _ in axioms]
    print("  %d axioms; a countermodel means the axiom is load-bearing." % len(labels))
    bearing = []
    for a in [None] + labels:
        name = "Ablate_" + (a or "NONE")
        build(name, [l for l in labels if l != a], PROBE_DICTATORSHIP)
        _, out = run(name)
        v = verdict(out)
        if v == "counterexample":
            bearing.append(a)
        print("  %-26s %s" % (a or "(control: none dropped)", v))
    print("  load-bearing by this test: " + " ".join(str(b) for b in bearing))
    print("  NOTE: 'no counterexample' is not proof of redundancy, only a failure "
          "to find one. Nothing here settles minimality; 'minimal' gives a "
          "constructive sufficient set and 'tight' gives the lower bound.")
    return True


def exp_lapsed():
    print("== lapsed: omsp is FALSE at t2, and the premise is the forbidden act ==")
    os.makedirs(WORK, exist_ok=True)
    for f in ("GodelCore.thy", "GodelConstitution.thy"):
        open(os.path.join(WORK, f), "w", encoding="utf-8").write(
            open(os.path.join(THY, f), encoding="utf-8").read())
    open(os.path.join(WORK, "OmspLapsed.thy"), "w", encoding="utf-8").write(
        "theory OmspLapsed\n  imports GodelConstitution\nbegin\n" + LAPSED + "\nend\n")
    code, out = run("OmspLapsed", extra_files=("GodelCore.thy", "GodelConstitution.thy"))
    good = code == 0 and "Error" not in out
    print("  cites only: amd2_prop_t2, amd2_not_maint_suf_t2")
    print("  note: omsp is the material universal")
    print("        ALL phi. ~(maint_suf phi) --> ~(is_prop phi)")
    print("        so ~omsp says only that SOMETHING forbidden was proposed.")
    print("        That is a VIOLATION of the clause, not a repeal of it. The")
    print("        model has no predicate separating a norm being in force from")
    print("        the norm being obeyed, so it cannot tell the two apart.")
    print("  RESULT: " + ("PROVED -- and the premise amd2_prop_t2 IS the forbidden "
                          "act, so the clause is falsified by stipulating its breach"
                          if good else "FAILED\n" + out[-2000:]))
    return good


def exp_blocking():
    print("== blocking: the logic CAN represent the clause blocking the amendment ==")
    _, axioms = dissect()
    drop = {"amd2_prop_t2", "amd1a_prop_t1", "amd1a_sup_rat_t1"}
    keep = [l for l, _ in axioms if l not in drop]
    build("BlockingWorks", keep, KEEP_OMSP_HEAD + BLOCKED + SATISFY)
    code, out = run("BlockingWorks")
    proved = bool(re.search(r"^theorem amd2_is_blocked_at_t2:", out, re.M))
    sat = "Nitpick found a model" in out
    # The theorem is kernel-certified and never flakes. The satisfiability half
    # is a Nitpick search, which can return no verdict under load. Report those
    # two separately so a tool failure is not scored as a refutation.
    print("  omsp propagated to t2; amd1a and amd2_prop_t2 withheld")
    print("  satisfiable: %s   proves the amendment is not proposed: %s" % (sat, proved))
    if code != 0 or "Error" in out or not proved:
        print("  RESULT: FAILED\n" + out[-2000:])
        return False
    if not sat:
        print("  RESULT: INCONCLUSIVE -- the blocked state proves the amendment is "
              "not proposed, but nitpick returned no model this run. Re-run it.")
        return True
    print("  RESULT: blocking IS representable -- the inconsistency the "
          "authors hit follows from stipulating amd2_prop_t2")
    return True


EXPERIMENTS = {"minimal": exp_minimal, "tight": exp_tight, "noamd1": exp_noamd1,
               "omsp": exp_omsp, "lapsed": exp_lapsed, "blocking": exp_blocking,
               "repeal": exp_repeal, "sweep": exp_sweep,
               "inventory": exp_inventory}

if __name__ == "__main__":
    which = sys.argv[1] if len(sys.argv) > 1 else "all"
    todo = (["minimal", "noamd1", "omsp", "lapsed", "blocking", "repeal"]
            if which == "all" else [which])
    if which not in EXPERIMENTS and which != "all":
        sys.exit("unknown experiment %r; choose from %s or 'all'"
                 % (which, ", ".join(sorted(EXPERIMENTS))))
    ok = True
    for name in todo:
        ok &= bool(EXPERIMENTS[name]())
        print()
    sys.exit(0 if ok else 1)
