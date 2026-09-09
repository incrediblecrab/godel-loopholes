"""Bounded SMT cross-check of the explicit Article V transition enumerator.

The amendment effect catalogue is shared specification data. Guards, frames and
transition search are separately encoded here; that checks implementation, not
the shared legal interpretation. Stuttering pads shorter paths to the bound.
"""

from dataclasses import dataclass

import z3

from article_v_model import (
    Amendment,
    Policy,
    Screening,
    Step,
    Suffrage,
    Support,
    Target,
    amendment_effect,
    reaches,
    replay,
)


BOOLEAN_FIELDS = (
    "proviso", "equal_senate", "legislative_independence",
    "judicial_independence", "executive_elections",
)
FIELDS = (*BOOLEAN_FIELDS, "ratifiers_required")


@dataclass(frozen=True)
class SMTResult:
    status: str
    steps: tuple[Step, ...] = ()
    reason: str | None = None


def _substantive_guard(before, after, policy: Policy, support: Support):
    guards = []
    if not policy.allow_threshold_change:
        guards.append(after["ratifiers_required"] == before["ratifiers_required"])
    if policy.democracy_floor:
        for field in (
            "legislative_independence", "judicial_independence", "executive_elections",
        ):
            guards.append(z3.Implies(before[field], after[field]))
    all_consent = len(support.consenters) == support.states
    if policy.self_entrenched and not all_consent:
        guards.append(z3.Implies(before["proviso"], after["proviso"]))
    if support.states - 1 not in support.consenters:
        guards.append(z3.Not(z3.And(
            before["proviso"], before["equal_senate"], z3.Not(after["equal_senate"]),
        )))
    if policy.suffrage == Suffrage.FUNCTIONAL and not all_consent:
        guards.append(z3.Not(z3.And(
            before["proviso"], before["legislative_independence"],
            z3.Not(after["legislative_independence"]),
        )))
    return z3.And(*guards)


def _goal(variables, target: Target):
    if target == Target.CONCENTRATED_POWERS:
        return z3.And(
            z3.Not(variables["legislative_independence"]),
            z3.Not(variables["judicial_independence"]),
        )
    if target == Target.EXECUTIVE_ELECTORAL_LOCK:
        return z3.Not(variables["executive_elections"])
    if target == Target.UNEQUAL_SENATE:
        return z3.Not(variables["equal_senate"])
    raise ValueError(f"Unknown target: {target!r}")


def solve(
    policy: Policy,
    support: Support,
    target: Target | None,
    max_steps: int = 4,
    alphabet: tuple[Amendment, ...] = tuple(Amendment),
    timeout_ms: int = 30_000,
) -> SMTResult:
    if max_steps < 0 or timeout_ms < 1:
        raise ValueError("The bound must be nonnegative and timeout must be positive")
    if len(set(alphabet)) != len(alphabet):
        raise ValueError("The amendment alphabet must not contain duplicates")
    solver = z3.Solver()
    solver.set(timeout=timeout_ms)
    variables = [
        {
            **{field: z3.Bool(f"{field}_{time}") for field in BOOLEAN_FIELDS},
            "ratifiers_required": z3.Int(f"required_{time}"),
        }
        for time in range(max_steps + 1)
    ]
    pending = [z3.Int(f"pending_{time}") for time in range(max_steps + 1)]
    choices = [z3.Int(f"choice_{time}") for time in range(max_steps)]
    solver.add(pending[0] == 0)
    for field in BOOLEAN_FIELDS:
        solver.add(variables[0][field])
    solver.add(variables[0]["ratifiers_required"] == (3 * support.states + 3) // 4)
    congress = all(
        2 * vote.present > vote.seats and 3 * vote.yes >= 2 * vote.present
        for vote in (support.house, support.senate)
    )
    width = len(alphabet)
    for time, choice in enumerate(choices):
        before, successor = variables[time], variables[time + 1]
        unchanged = z3.And(*(successor[field] == before[field] for field in FIELDS))
        alternatives = [z3.And(
            choice == 0, pending[time + 1] == pending[time], unchanged,
        )]
        for index, amendment in enumerate(alphabet, 1):
            effect = amendment_effect(amendment, support.states)
            after = {field: effect.get(field, before[field]) for field in FIELDS}
            substantive = _substantive_guard(before, after, policy, support)
            alternatives.append(z3.And(
                choice == index,
                pending[time] == 0,
                congress,
                substantive if policy.screening == Screening.PROPOSAL else True,
                pending[time + 1] == index,
                unchanged,
            ))
            alternatives.append(z3.And(
                choice == width + index,
                pending[time] == index,
                len(support.ratifiers) >= before["ratifiers_required"],
                substantive if policy.screening == Screening.RATIFICATION else True,
                pending[time + 1] == 0,
                *(successor[field] == after[field] for field in FIELDS),
            ))
            alternatives.append(z3.And(
                choice == 2 * width + index,
                pending[time] == index,
                pending[time + 1] == 0,
                unchanged,
            ))
        solver.add(z3.Or(*alternatives))
    if target is not None:
        solver.add(_goal(variables[-1], target))
    verdict = solver.check()
    if verdict == z3.unsat:
        return SMTResult("UNSAT")
    if verdict == z3.unknown:
        return SMTResult("UNKNOWN", reason=solver.reason_unknown())
    if verdict != z3.sat:
        raise RuntimeError(f"Unexpected solver result: {verdict}")
    model = solver.model()
    steps = []
    for choice in choices:
        code = model.eval(choice).as_long()
        if code == 0:
            continue
        phase = ("propose", "ratify", "withdraw")[(code - 1) // width]
        amendment = alphabet[(code - 1) % width]
        steps.append(Step(phase, amendment))
    endpoint = replay(policy, support, steps)
    if target is not None and not reaches(endpoint, target):
        raise AssertionError("SMT witness failed concrete replay")
    return SMTResult("SAT", tuple(steps))
