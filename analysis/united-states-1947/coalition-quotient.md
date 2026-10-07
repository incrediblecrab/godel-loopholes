# An exact quotient of fixed coalition inputs

**October 7, 2026.** The existing Article V model now has a complete reachability classification for its three terminal predicates over arbitrary fixed ratifier and consenter subsets, under its original interpretation grid. Previously the main grid tested only three selected prefix profiles in which ratification and consent were assigned to the same states. No legal rule, amendment effect, or terminal predicate was changed.

This is an instrument result about the declared finite model. It is not a constitutional loophole, a judgment about legally valid consent, or evidence about Gödel's private argument. The corpus review suggested examining what a representation preserves; the result below follows from this project's existing model, not from an OpenAI theorem about law.

## The quotient

Fix the state universe, congressional vote profile, ratification mode, policy, and action alphabet. Let $R$ be the ratifying states, let $C$ be the consenting states, and let $T$ be the initial ratification threshold returned by `initial_state`. In the 1947 model the universe has forty-eight states and $T=36$. The model singles out state 47 for its unequal-Senate action.

Only the following observations of $R$ and $C$ enter the transition guards:

| Ratifiers | Consent |
| --- | --- |
| $|R|=0$ | The designated affected state is absent from $C$. |
| $0<|R|<T$ | The designated state is in $C$, but $C$ is not the whole universe. |
| $|R|\ge T$ | $C$ is the whole universe. |

These columns vary independently, giving nine sufficient classes. They are not claimed to be the smallest quotient for every policy or for reachability from the initial state alone. In particular, the zero and positive-below-threshold classes have the same constitutional outcomes from the initial state, but differ at a state whose threshold has already become one.

The representative replaces $R$ with a prefix of size zero, one, or $T$, and replaces $C$ with the empty set, the designated singleton, or the whole universe. It preserves the other support fields. This preserves transition behavior and the applicability of action-labeled witnesses, **not** the input's raw coalition size, overlap, political cost, or probability. Those quantities cannot be inferred from the representative.

## Why arbitrary fixed subsets reduce to these classes

The proof uses two invariants that must be reconsidered if the model changes.

First, the required ratifier count is always in $\{1,T\}$. Initially it is $T$; the only threshold effects set it to one or restore $T$; all other actions preserve it. Each ratifier class therefore fixes the truth of both possible ratification comparisons. Zero passes neither; positive-below-threshold passes only one; qualifying support passes both.

Second, every consent test concerns either no deprived state, the designated singleton, or the whole universe. The equal-suffrage action names the singleton. Functional deprivation names every state, and self-entrenched repeal tests unanimity. The union of any of these sets remains in the same three-set family. The consent classes fix all these subset tests.

Proposal-vote conditions are preserved because canonicalization does not change the congressional votes. Substantive guards are equal by the consent argument; ratification-count guards are equal by the threshold argument. Pending-proposal requirements and amendment effects do not otherwise depend on $R$ or $C$. Thus, at the same constitutional and protocol state, the same labeled operation is rejected for the same reason or leads to the same successor. Induction on operations gives the same complete finite transition graph and the same witnesses for supports in one class.

The support sets must remain fixed throughout the path. This argument does not merge histories in which coalitions change between operations, admit new states, alter which states are deprived, or change congressional attendance. Those are different models.

## Closed-form classification

Assume the original congressional proposal votes pass. If $|R|<T$, none of the three targets is reachable: no first ratification can occur, and proposal and withdrawal cannot change the threshold. A threshold-lowering amendment cannot authorize itself.

For $|R|\ge T$, the classification is:

| Target | Necessary and sufficient condition in this model | Shortest path |
| --- | --- | --- |
| End executive elections | No implicit democracy floor. | One proposal and ratification. |
| Unequal Senate suffrage | The designated state consents, or the proviso is not self-entrenched. | One proposal and ratification if the designated state consents; otherwise repeal, then enact the change. |
| Concentrate powers | No democracy floor, and at least one of: formal rather than functional suffrage; unanimous consent; no self-entrenchment. | One proposal and ratification under formal suffrage or unanimous consent; otherwise repeal, then concentrate. |

If congressional proposal cannot pass, no target is reachable from the initial state. The “otherwise” paths in the table take two separate ratifications, not an instrument that uses its own repeal. Each ratification requires a prior proposal, so the displayed paths have two or four operations.

For necessity, each target requires the first relevant effect that removes the protected property. The democracy floor blocks the relevant effects regardless of prior changes. Where the proviso applies, changing the designated state's suffrage requires its consent unless the proviso was previously repealed. Functional concentration likewise requires unanimity while the proviso remains. Self-entrenchment blocks the necessary repeal without unanimity. The action catalogue has no alternative effect that bypasses these guards. For sufficiency, the one- or two-amendment paths in the table satisfy the existing guards. Neither proposal-versus-ratification screening nor permission to change the numerical threshold shortens these paths under fixed support.

The pre-existing small interpretation table already showed parts of this pattern. The addition is a unified classification, with the experimental prefix/same-coalition restriction removed and the required quotient stated explicitly. It is not discovery of the underlying consent distinction, which earlier unit tests already exercised.

## Executed evidence

The canonical record is [`search/coalition_quotient_results.json`](search/coalition_quotient_results.json). It contains **144 configurations and 432 target queries**: sixteen original policies times nine coalition classes, with three targets each. Saturated BFS reports **84 reachable and 348 unreachable** target queries. All 432 agree with the existing independently encoded SMT model within its four-operation bound, and the closed-form classification matches every BFS answer and shortest length.

Unreachability at every path length in the declared finite graph comes from BFS saturation, not the bounded SMT result. The quotient proof extends representative results to other fixed supports. The representative runs also preserve the original 48 configurations' graph statistics and target records exactly.

Two separate solver checks seek counterexamples to the arithmetic and consent reductions. The first ranges over arbitrary valid ratifier counts and both possible thresholds. The second uses forty-eight-bit consent sets and all three permitted deprivation sets. Both return `UNSAT`. Dropping the zero-versus-positive distinction, affected-state identity, or unanimity distinction instead produces a counterexample and a failing command. These checks support the written argument; they are not an Isabelle kernel proof of the Python implementation or its legal correspondence.

The class sizes sum to all pairs of subsets of the fixed universe. This is a coverage calculation, not a count of individually enumerated coalitions, independently discovered paths, or plausible political situations. No fraction of favorable cells is interpreted as a probability.

## Reproduction and boundaries

From the repository root, using the existing shared environment:

```bash
.venv/bin/python -B -m unittest discover -s analysis/united-states-1947/search -p 'test_coalition_quotient.py' -v
.venv/bin/python -B analysis/united-states-1947/search/coalition_quotient.py --check
.venv/bin/python -B analysis/united-states-1947/search/coalition_quotient.py --plant consent-id
```

The last command must display a counterexample and exit one. The other plants are `threshold` and `consent-all`. A solver timeout is inconclusive, not a successful negative control. Use `--write` only to deliberately regenerate the artifact after reviewing changes.

The runner reads the original grid as its scope source and rejects changed baseline source hashes. It imports the existing evaluator and transition model; no parallel legal model or proof-assistant port is introduced. The artifact also records the new source hashes and environment. Small-universe exhaustive subset enumeration checks the class-size formulas, while transition controls and the original model's tests exercise the correspondence.

The project remains without a verified lawful-collapse path or historical attribution. The legal interpretation, hypothetical amendment effects, fixed state universe, fixed support over time, and finite action alphabet remain material assumptions. A changing-coalition model or a different deprivation rule needs a new argument, not reuse of this verdict.
