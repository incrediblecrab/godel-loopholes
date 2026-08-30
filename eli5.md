# Explain it like I'm five

## The story

In 1947 a mathematician named Kurt Gödel was studying for his U.S. citizenship test. He was probably the greatest logician who ever lived, and he read the Constitution the way he read everything else — looking for gaps.

He found one. Or thought he did. He told his friend Oskar Morgenstern that the Constitution had "inner contradictions," and that someone could use them to become a dictator **without breaking a single rule**.

He took the exam on December 5, 1947, in Trenton, New Jersey. Einstein and Morgenstern drove him there and spent the whole trip begging him not to bring it up. He brought it up. The examiner shut him down, and Gödel became a citizen on April 2, 1948.

Then he never wrote it down. Not in his letters, not in his notes, nowhere. The only record is a memo Morgenstern typed **twenty-four years later**, from memory, which begins by admitting he hadn't checked his diaries. Morgenstern doesn't say which part of the Constitution Gödel meant. A few lines later he adds that he didn't think Gödel was right.

So: the smartest logic guy in history said he found a hole, gave no details, and the one witness was fuzzy and skeptical. That's the puzzle.

## What "loophole" means here

It does **not** mean a coup. It does not mean someone breaking the law and getting away with it.

Think of a board game. A coup is flipping the table. A loophole is finding a legal move — one the rulebook plainly allows — that lets you win in a way the people who wrote the rules would be horrified by. Nobody cheated. The rules just permitted something nobody noticed.

That distinction is the whole project. If any step requires breaking a rule, we haven't found anything. Governments get overthrown illegally all the time; that's not interesting and it's not what Gödel claimed.

The scary version is that you *can't fix this by enforcing the rules harder*. Enforcing the rules is exactly what the attacker is doing.

## Why anyone thinks this is possible

Because it has actually happened, more than once, and each time differently.

**Germany, 1933.** Hitler used the amendment procedure itself. The Weimar constitution said you could change it with a two-thirds vote. So they took a two-thirds vote and changed it into something that let one man make law. Every box was ticked. The rule was fine on its own terms and still authorized its own destruction.

**Austria, 1933.** This one is sneakier and it's the one Gödel actually lived through. The government didn't use the constitution at all. They reached *outside* it, to a forgotten emergency economic law from 1917 that nobody had ever bothered to repeal, and governed through that. If you were only reading the constitution, you would have seen nothing wrong.

**Italy, 1925.** The constitution was never touched. Not one of its eighty-four articles was amended. They just passed ordinary laws until the state was hollowed out around it. A photo of the document in 1848 and a photo in 1925 look identical while everything real changed.

Gödel was Austrian. He watched his own country do this. When the examiner asked what kind of government he'd lived under, he said it was a republic whose constitution "was such that it finally was changed into a dictatorship" — and then offered to prove America could do the same.

Those three cases are our test set, and we use them as a *filter for our own methods*. Any technique we invent has to rediscover all three. A method that only reads constitutional text catches Germany and is blind to Austria and Italy, and that tells us the method is too narrow — before we ever point it at an open question.

## The two ways in

**Route one: words.** Find a place where the text genuinely doesn't say what everyone assumes.

This sounds like a stretch until you see it happen. In 2017 a Maine dairy lost an overtime case because of a **missing comma**, and settled the following year for $5 million across 127 drivers. The law listed activities exempt from overtime, and without a comma in the list it was unclear whether "packing for shipment or distribution" meant one activity or two. The court's opinion literally opens: "For want of a comma, we have this case."

So: commas move money and change what a law means. And this isn't only a problem for obscure state statutes — we found the same thing in the Bill of Rights, without looking for it.

We compared Amendments I through X across six independent witnesses, expecting them to be identical. On wording they agree completely, and three differences turned up anyway — every one of them a comma or a letter. The Government Publishing Office prints the First Amendment as "**of** the right of the people peaceably to assemble" where every other source reads "**or** the right." One letter. But "or" makes assembly its own protected thing, while "of" quietly tucks it under freedom of the press. Yale's Avalon Project silently drops two commas, including the one that hinges the Seventh Amendment. And the Statutes at Large prints the Second Amendment twice, not identically, with one comma where the parchment has three.

Nobody planted those for us to find. We were just checking that our copies matched.

**Route two: math.** Treat the Constitution like a machine with rules for rewriting itself, and ask what states it can reach.

Article V is the interesting part. It's the rule for changing the Constitution — and it doesn't protect itself. You can use Article V to amend Article V. So one reading is: any lock on the door can be removed, because the procedure for removing locks is itself just another lock.

## What we've actually done so far

Here's the honest scoreboard. This section matters more than the exciting parts.

**We proved that somebody else's proof works.** Two researchers, Zahoransky and Benzmüller, already fed a version of this argument into a proof-checking computer program in 2019. We retyped their entire model by hand and ran it. It works — the computer confirms all three of their conclusions.

**Then we checked whether that meant anything.** This is the part people skip. In logic there's a nasty trap: if your starting assumptions secretly contradict each other, then the computer will "prove" *literally anything you ask it*, including nonsense. A proof from broken assumptions looks exactly like a real proof.

So we asked the computer to hunt for contradictions in the assumptions. It found none, and it built actual working examples showing the opposite conclusions are *not* provable. Meaning: the proof is real, not an artifact of broken setup.

**And we found the catch.** Their model says: *if* you can amend Article V, dictatorship follows lawfully. But look closely at how they made that first step happen — they didn't model it at all. They just **deleted an assumption** to make the amendment appear. They admit this in the paper.

That matters enormously. The hard part of the argument is the part they skipped. In 1947 amending the Constitution required 36 of the 48 states to agree. Their model doesn't contain states, or counting, or ratification, at all. So the published formal proof doesn't establish the thing that's actually hard.

**A mistake we made, kept on purpose.** We asked a math solver for the minimum number of Representatives needed to pass an amendment. It said 219. Our hand calculation said 218. The solver was right and *our label was wrong* — we'd asked it a subtly different question than the one we wrote down in English next to the answer.

Nothing was broken. The computer answered exactly what we typed. The English sentence we attached to the output claimed something the math didn't say. We wrote this down because it's the single easiest way to fool yourself with these tools, and it's invisible: the output is correct, the sentence is wrong, and no computer will ever catch that for you.

**And then we did it again.** Our own testing script had a bug where a computer that *ran out of time* got reported as a computer that *said no*. It printed a scary "the assumptions are inconsistent!" warning about one run in six, which was simply false — the tool hadn't answered at all. Same error, second time. Now the script has three answers instead of two: yes, no, and **didn't finish** — because "no answer" is not an answer.

## The thing we're most afraid of

AI can generate enormous amounts of confident, well-written, plausible analysis very fast. Almost none of it would be worth anything, and it would all *look* exactly like the real thing.

So the rules here are deliberately annoying:

- Every claim cites the actual historical document, with a specific edition.
- We write down what we got **wrong**, and the dead ends, in the same detail as the wins.
- Nothing counts as a finding unless we can also state exactly how someone would prove us wrong.
- We don't trust a tool until it has reproduced a result somebody else already published.
- Anything we haven't verified gets labeled as unverified, even when that's less impressive.

There's a script, `verify.sh`, that re-runs every single computational claim in this repository from scratch. Six of its checks are **designed to fail** — a deliberately false statement the computer must reject. If those ever start "passing," the whole harness is lying and everything else it says is worthless.

## What's in here

- **`corpus/`** — the actual historical texts, with receipts for where each came from.
- **`academia/`** — what's already been published. We read the literature before inventing anything.
- **`method/`** — how to look. Written so a human could do it by hand with no computer.
- **`analysis/`** — what we found by looking, one folder per country-and-year.
- **`TOOLING.md`** and **`verify.sh`** — the software, and the proof it works.

## Are we going to find it?

Probably not, in the sense of "the exact thing Gödel had in mind." That's likely gone forever — he never wrote it down, and the one witness was working from a twenty-four-year-old memory he himself doubted.

But that was never really the point. The useful question isn't *what did Gödel think?* It's *does the Constitution actually contain a lawful path to its own destruction, and can we find it by reading carefully?* That question is answerable, and it doesn't depend on channeling a dead man.

And if the method works on one country, it works on all of them. That's the long game: a public, checkable record of the structural weak points in the world's founding documents, with every step laid out so that anyone can follow the reasoning — or tear it apart.
