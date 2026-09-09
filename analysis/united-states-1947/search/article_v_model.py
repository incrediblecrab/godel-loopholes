"""An explicit, finite Article V interpretation model, not a legal decision procedure.

Only ratification changes the constitution. Unchanged fields persist. The action
alphabet, consent assumptions and terminal predicates are intentionally exposed.
See ../bounded-article-v-search.md for the correspondence and scope limitations.
"""

from collections import deque
from dataclasses import asdict, dataclass, replace
from enum import Enum
from typing import Iterator


class Suffrage(str, Enum):
    FORMAL = "formal"
    FUNCTIONAL = "functional"


class Screening(str, Enum):
    PROPOSAL = "proposal"
    RATIFICATION = "ratification"


class Amendment(str, Enum):
    REPEAL_PROVISO = "repeal_proviso"
    RESTORE_PROVISO = "restore_proviso"
    CONCENTRATE = "concentrate_powers"
    RESTORE_POWERS = "restore_separation"
    END_ELECTIONS = "end_executive_elections"
    RESTORE_ELECTIONS = "restore_executive_elections"
    UNEQUAL_SENATE = "unequal_senate"
    RESTORE_EQUALITY = "restore_equal_senate"
    LOWER_THRESHOLD = "lower_ratification_threshold"
    RESTORE_THRESHOLD = "restore_ratification_threshold"
    REPEAL_AND_CONCENTRATE = "repeal_and_concentrate"
    LOWER_AND_CONCENTRATE = "lower_threshold_and_concentrate"


class Target(str, Enum):
    CONCENTRATED_POWERS = "concentrated_powers"
    EXECUTIVE_ELECTORAL_LOCK = "executive_electoral_lock"
    UNEQUAL_SENATE = "unequal_senate"


@dataclass(frozen=True)
class Policy:
    suffrage: Suffrage = Suffrage.FUNCTIONAL
    self_entrenched: bool = False
    democracy_floor: bool = False
    screening: Screening = Screening.RATIFICATION
    allow_threshold_change: bool = True

    def to_dict(self) -> dict:
        return {
            **asdict(self),
            "suffrage": self.suffrage.value,
            "screening": self.screening.value,
        }


@dataclass(frozen=True)
class Votes:
    seats: int
    present: int
    yes: int

    def __post_init__(self) -> None:
        if not 0 <= self.yes <= self.present <= self.seats or self.seats < 1:
            raise ValueError("Votes require 0 <= yes <= present <= seats and seats > 0")

    def can_propose(self) -> bool:
        return 2 * self.present > self.seats and 3 * self.yes >= 2 * self.present


@dataclass(frozen=True)
class Support:
    states: int
    ratifiers: frozenset[int]
    consenters: frozenset[int]
    house: Votes
    senate: Votes
    mode: str = "legislatures"

    def __post_init__(self) -> None:
        if self.states < 1:
            raise ValueError("There must be at least one state")
        universe = frozenset(range(self.states))
        if not self.ratifiers <= universe or not self.consenters <= universe:
            raise ValueError("Ratification and consent must identify existing states")
        if self.mode not in ("legislatures", "conventions"):
            raise ValueError("Ratification mode must be legislatures or conventions")

    @property
    def all_states(self) -> frozenset[int]:
        return frozenset(range(self.states))


@dataclass(frozen=True)
class Constitution:
    proviso: bool = True
    equal_senate: bool = True
    legislative_independence: bool = True
    judicial_independence: bool = True
    executive_elections: bool = True
    ratifiers_required: int = 36


@dataclass(frozen=True)
class State:
    constitution: Constitution
    pending: Amendment | None = None


@dataclass(frozen=True)
class Step:
    phase: str
    amendment: Amendment

    def label(self) -> str:
        return f"{self.phase}:{self.amendment.value}"


class InvalidTransition(ValueError):
    pass


def initial_state(states: int = 48) -> State:
    if states < 1:
        raise ValueError("There must be at least one state")
    return State(Constitution(ratifiers_required=(3 * states + 3) // 4))


def quorum_votes(seats: int) -> Votes:
    if seats < 1:
        raise ValueError("A chamber must have at least one seat")
    present = seats // 2 + 1
    return Votes(seats, present, (2 * present + 2) // 3)


def support_profile(count: int, states: int = 48, mode: str = "legislatures") -> Support:
    if not 0 <= count <= states:
        raise ValueError("Support count must be between zero and the number of states")
    coalition = frozenset(range(count))
    return Support(states, coalition, coalition, quorum_votes(435), quorum_votes(2 * states), mode)


def amendment_effect(amendment: Amendment, states: int) -> dict[str, bool | int]:
    effects: dict[Amendment, dict[str, bool | int]] = {
        Amendment.REPEAL_PROVISO: {"proviso": False},
        Amendment.RESTORE_PROVISO: {"proviso": True},
        Amendment.CONCENTRATE: {
            "legislative_independence": False, "judicial_independence": False,
        },
        Amendment.RESTORE_POWERS: {
            "legislative_independence": True, "judicial_independence": True,
        },
        Amendment.END_ELECTIONS: {"executive_elections": False},
        Amendment.RESTORE_ELECTIONS: {"executive_elections": True},
        Amendment.UNEQUAL_SENATE: {"equal_senate": False},
        Amendment.RESTORE_EQUALITY: {"equal_senate": True},
        Amendment.LOWER_THRESHOLD: {"ratifiers_required": 1},
        Amendment.RESTORE_THRESHOLD: {"ratifiers_required": (3 * states + 3) // 4},
    }
    effects[Amendment.REPEAL_AND_CONCENTRATE] = {
        **effects[Amendment.REPEAL_PROVISO], **effects[Amendment.CONCENTRATE],
    }
    effects[Amendment.LOWER_AND_CONCENTRATE] = {
        **effects[Amendment.LOWER_THRESHOLD], **effects[Amendment.CONCENTRATE],
    }
    return effects[amendment]


def amended(constitution: Constitution, amendment: Amendment, states: int) -> Constitution:
    return replace(constitution, **amendment_effect(amendment, states))


def substantive_objections(
    before: Constitution, amendment: Amendment, policy: Policy, support: Support,
) -> tuple[str, ...]:
    after = amended(before, amendment, support.states)
    objections = []
    if not policy.allow_threshold_change and after.ratifiers_required != before.ratifiers_required:
        objections.append("amendment-rule-change-disallowed")
    if policy.democracy_floor and (
        (before.legislative_independence and not after.legislative_independence)
        or (before.judicial_independence and not after.judicial_independence)
        or (before.executive_elections and not after.executive_elections)
    ):
        objections.append("implicit-democracy-floor")
    if before.proviso:
        if policy.self_entrenched and not after.proviso and support.consenters != support.all_states:
            objections.append("proviso-repeal-needs-every-state-consent")
        deprived = frozenset()
        if before.equal_senate and not after.equal_senate:
            deprived |= frozenset({support.states - 1})
        if (
            policy.suffrage == Suffrage.FUNCTIONAL
            and before.legislative_independence
            and not after.legislative_independence
        ):
            deprived |= support.all_states
        if not deprived <= support.consenters:
            objections.append("deprived-state-without-consent")
    return tuple(objections)


def rejection(state: State, step: Step, policy: Policy, support: Support) -> str | None:
    if step.phase == "propose":
        if state.pending is not None:
            return "another-proposal-is-pending"
        if not support.house.can_propose() or not support.senate.can_propose():
            return "congressional-proposal-threshold"
        if policy.screening == Screening.PROPOSAL:
            objections = substantive_objections(state.constitution, step.amendment, policy, support)
            if objections:
                return ";".join(objections)
        return None
    if step.phase not in ("ratify", "withdraw"):
        return "unknown-phase"
    if state.pending != step.amendment:
        return "no-matching-proposal"
    if step.phase == "withdraw":
        return None
    if len(support.ratifiers) < state.constitution.ratifiers_required:
        return "state-ratification-threshold"
    if policy.screening == Screening.RATIFICATION:
        objections = substantive_objections(state.constitution, step.amendment, policy, support)
        if objections:
            return ";".join(objections)
    return None


def apply_step(state: State, step: Step, policy: Policy, support: Support) -> State:
    reason = rejection(state, step, policy, support)
    if reason is not None:
        raise InvalidTransition(f"{step.label()}: {reason}")
    if step.phase == "propose":
        return State(state.constitution, step.amendment)
    if step.phase == "withdraw":
        return State(state.constitution)
    return State(amended(state.constitution, step.amendment, support.states))


def candidates(state: State, alphabet: tuple[Amendment, ...]) -> Iterator[Step]:
    if state.pending is None:
        for amendment in alphabet:
            yield Step("propose", amendment)
    else:
        yield Step("ratify", state.pending)
        yield Step("withdraw", state.pending)


def reaches(state: State, target: Target) -> bool:
    constitution = state.constitution
    if target == Target.CONCENTRATED_POWERS:
        return not constitution.legislative_independence and not constitution.judicial_independence
    if target == Target.EXECUTIVE_ELECTORAL_LOCK:
        return not constitution.executive_elections
    if target == Target.UNEQUAL_SENATE:
        return not constitution.equal_senate
    raise ValueError(f"Unknown target: {target!r}")


@dataclass
class Exploration:
    parents: dict[State, tuple[State, Step] | None]
    legal_edges: int
    rejected_edges: int

    def shortest_path(self, target: Target) -> list[Step] | None:
        endpoint = next((state for state in self.parents if reaches(state, target)), None)
        if endpoint is None:
            return None
        steps = []
        while self.parents[endpoint] is not None:
            parent, step = self.parents[endpoint]
            steps.append(step)
            endpoint = parent
        return list(reversed(steps))


def explore(
    policy: Policy, support: Support, alphabet: tuple[Amendment, ...] = tuple(Amendment),
) -> Exploration:
    start = initial_state(support.states)
    parents: dict[State, tuple[State, Step] | None] = {start: None}
    queue = deque([start])
    legal_edges = rejected_edges = 0
    while queue:
        state = queue.popleft()
        for step in candidates(state, alphabet):
            if rejection(state, step, policy, support) is not None:
                rejected_edges += 1
                continue
            legal_edges += 1
            successor = apply_step(state, step, policy, support)
            if successor not in parents:
                parents[successor] = (state, step)
                queue.append(successor)
    return Exploration(parents, legal_edges, rejected_edges)


def replay(policy: Policy, support: Support, steps: list[Step]) -> State:
    state = initial_state(support.states)
    for step in steps:
        state = apply_step(state, step, policy, support)
    return state
