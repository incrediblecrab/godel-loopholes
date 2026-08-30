# Gödel loopholes

Kurt Gödel proved that any formal system strong enough to do arithmetic contains true statements it cannot prove. In 1947 he studied the Constitution for his citizenship exam, read it the way he read formal systems, and decided it had a flaw of its own — a way to turn the country into a dictatorship without anyone breaking a rule.

He took the exam on December 5, 1947, in Trenton, New Jersey. Einstein and Oskar Morgenstern came as his witnesses, and they spent the drive down telling him not to bring it up. He brought it up. The examiner cut him off, and Gödel swore the oath on April 2, 1948.

Gödel never wrote the argument down. Everything we have comes from a memo Morgenstern dictated on September 13, 1971, twenty-four years later, opening with the admission that he was working from memory and had not checked his diaries.

> He rather excitedly told me that in looking at the Constitution, to his distress he had found some inner contradictions and that he could show how in a perfectly legal manner it would be possible for somebody to become a dictator and set up a Fascist regime, never intended by those who drew up the Constitution.

Morgenstern does not say which part of the Constitution Gödel meant, and a few lines later he adds that he doubted Gödel was right. What survives is the phrase "in a perfectly legal manner." Gödel was claiming an attack that follows the rules, and a rule-following attack is the kind you cannot patch by enforcing the rules harder.

Austria comes up in the memo too. The examiner asked what sort of government Gödel had lived under, and Gödel answered that it was a republic whose constitution "was such that it finally was changed into a dictatorship." Then he said the same thing could happen here, and offered to prove it.

## Hypothesis

The Constitution contains at least one path where people follow its rules and arrive somewhere the ratifiers would have called its destruction. We think we can find that path by reading the text. Working out what Gödel actually had in mind is a separate job, and we do not need to finish it first.

If we can find it here, the same method should work on any founding document that has a written text and an amendment procedure. We want a public record of these holes across countries, with the reasoning laid out step by step so anyone can check it or knock it down.

New here, or want the version without the jargon? Start with `eli5.md`.

## Where this stands

**No loophole has been found.** The hypothesis above is unproved and the search has not produced a candidate path. Anything in this repo that reads like progress is progress on the *instruments*, not on the Constitution, and the files say so themselves.

What does exist is one machine-checked result about the only published formalization of Gödel's claim — Zahoransky and Benzmüller's Isabelle/HOL model. Their theorems reproduce exactly. Then, running ablations against the reproduction:

- `Dictatorship_t3` follows from **6 of the model's 51 axioms**, and those six are consistent. Two are generic amendment-procedure rules, two are bare temporal-successor facts, and two stipulate that the dictatorship amendment is proposed and supported. None is an equal-suffrage, entrenchment, Senate, or step-one axiom.
- **4 of the 6** are necessary to *every* possible proof, established by countermodels to the full theory minus each one. Six is irredundant but not proved minimum; the honest bound is 4 ≤ minimum ≤ 6.
- The four axioms encoding **Gödel's step one** — proposing and supporting the amendment that strips Article V's entrenchment clause — can be deleted and **every theorem and lemma published in the original still proves**, in a theory Nitpick confirms is still consistent. Two proof scripts break; none of those five propositions does.
- What the deletion *does* cost is exactly one proposition: `⌊is_rat amd1a⌋t2`, the ratification of the repeal itself, which the full theory entails and the reduced theory leaves **independent**. So step one is not free — it is just that no published result uses it.
- The reason: `amd1a` is extensionally equal to the negation of the entrenchment clause, provably without any of the model's non-definitional axioms. Its content is therefore already forced by the separate stipulation that the dictatorship amendment was proposed. The repeal event is represented and entailed; its normative effect is not what does the work.

The authors disclose the underlying design choice in both the thesis and the peer-reviewed paper. What is new here is the measurement of what it costs, which turns out to be nothing, and the diagnosis of why.

`analysis/united-states-1947/inert-manoeuvre.md` is the write-up. `./verify.sh` re-runs everything from scratch, including the slow lower-bound experiment: **88 checks, all passing**, on a clean checkout with Isabelle on PATH.

Every load-bearing number, date and quotation in this repository is owned by exactly one file, and `data/facts.json` records which. `tools/facts.py` asserts each value is actually present in the file named as its owner and that every derived number follows from the numbers it derives from; `tools/ssot_audit.py` reports facts told in more than one place so the canonical telling can be distinguished from a pointer to it. Section 6 of the harness runs both. The rule is that prose is authored per audience and may differ between a research note and a general-audience page, but values may not.

### Claims made here and later disproved

Kept visible on purpose, because a repo that only records its wins is not evidence of anything.

1. That `sup_rat` could be attacked by contraposition — refuted by a countermodel.
2. That the formalism *cannot represent a constraint blocking an amendment* — refuted by building the blocked state (`axiom_sweep.py blocking`).
3. That the six axioms are *minimal* — they are irredundant, which is weaker.
4. That the model *cannot tell repeal from violation* — refuted by proving `amd1a = ❙¬omsp` and the event `⌊is_rat amd1a⌋t2`.
5. That deleting Gödel's step one *loses five lemmas* — it loses two proof scripts and none of those five propositions.
6. That deleting Gödel's step one therefore costs **nothing** — false, and refuted by an experiment I had already run. It costs `⌊is_rat amd1a⌋t2`, which becomes independent.
7. That `amd1a = ❙¬omsp` is a *term identity* — it is extensional equality; `by (rule refl)` fails on that goal.
8. That *none of the six axioms is an Article V axiom* — two of them are the generic amendment procedure. That was classification by symbol name.

One shipped experiment was also **vacuous** for a period: the ablation emitted axioms before the definition they mentioned, Isabelle generalized the free variable, and the reduced theory silently became inconsistent while still printing every theorem as proved. Adversarial review caught it, not the harness. Every ablation now carries a mandatory consistency probe.
