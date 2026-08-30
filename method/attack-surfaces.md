# Attack surfaces

This file partitions the problem. Everything in `analysis/` is expected to say which class its candidate falls in, and a candidate that fits none of them is either a new class, which is a finding in itself, or confused.

## Where the authorizing norm sits

The primary partition is not what a step does but where the rule permitting it lives. Three classes, and they are exhaustive by construction: a norm is either in the constitution or not, and if it is not, the constitution either reaches it or does not.

**Class 1, inside.** The constitution itself authorizes the step. Germany is the clean case: an amendment rule with no substantive floor authorized a law that switched the amendment rule off. The full path from Article 76 through the Enabling Act is in `analysis/germany-1933/path-enabling-act.md`.

**Class 2, outside but reached through.** A clause in the constitution carries in, preserves, or defers to law that sits outside it. Austria is the case, and it is the one most likely to be missed. The chain is three documents long, only the first link is in the constitution, and the instrument at the end of it is an ordinary economic statute the constitution never names. The full path from Article 150 through the KWEG is in `analysis/austria-1920/path-kweg-bridge.md`.

**Class 3, outside and unreached.** The constitution does not govern the field at all, and ordinary legislation does the work. Italy is the case. The Statuto Albertino declared itself perpetual and irrevocable and its eighty-four articles were never amended; everything happened in ordinary statutes while the constitution sat untouched. The full analysis, and the reason every formal enumeration returns empty against a flexible constitution, is in `analysis/italy-1848/null-result-formal-route.md`.

The classes are not equally visible. A method that reads only constitutional text sees class 1 completely, sees class 2 only if it follows references outward, and is blind to class 3 by construction. This is why the three collapses are the test set and why Italy is the discriminating case: any procedure that recovers Germany and misses Italy has not been validated, it has been flattered.

## How a check fails

Given that a safeguard exists, the second partition asks which part of it gave way. A check has four components — a trigger, an operator who fires it, a scope, and a duration — so with the case where no check exists at all there are five ways to fail, and they are exhaustive over the anatomy.

**No check.** Weimar Article 76 carried no substantive limit whatever. Nothing was placed beyond amendment, there was no unamendable clause, and the entrenchment was purely procedural.

**The trigger is self-judged.** The condition that opens the power is assessed by the person who benefits from opening it. Nothing in Weimar Article 48 gave anyone but the President the judgment that public security was seriously disturbed.

**The operator can be disabled.** This is the failure that matters most and the one a naive method scores as safe. Both checks were textually sound, neither was ever amended or repealed, and both failed because the body that operates them can be stopped from sitting. The German instance is Step 3 of `analysis/germany-1933/path-enabling-act.md`; the Austrian instance, including the parliamentary resignation gap, is Step 5 of `analysis/austria-1920/path-kweg-bridge.md`.

**The scope is obeyed and evaded.** The limit is respected on the dimension it names while the effect is achieved on a dimension it does not. The Reichstag Fire Decree suspended exactly the seven rights articles Article 48(2) enumerated, scrupulously — but substituted *bis auf weiteres* for the constitution's *vorübergehend*, and that substitution is demonstrably deliberate. The full textual evidence is Step 1 of `analysis/germany-1933/path-enabling-act.md`.

**The duration is limited but renewable, or self-sealing.** A sunset restrains only an actor who will not hold the power at sunset. The sharper failure is a termination condition triggered by an event the power itself exists to prevent — such a condition is not a limit on the holder but a statement of what the holder must avoid. The Enabling Act's two sunset clauses are the textbook instance, analysed in `analysis/germany-1933/path-enabling-act.md` under "The limits that held and did not matter."

The consequence for method is a change of question. Asking whether a document contains checks is close to useless, because all three of these documents did. The question that separates them is who must be functioning for a given check to fire, and whether that person or body can be stopped by someone the check is aimed at.

## What this partition does not cover

Nothing here addresses whether a step is politically likely, and nothing here addresses conduct that breaks a rule. A takeover carried out by force is out of scope for this project by definition, and violence appears in these cases as the thing that made lawful steps effective rather than as a substitute for them. Where an analysis needs an extra-legal step to complete its chain, that is not a gap in this taxonomy. It is a disqualified candidate.
