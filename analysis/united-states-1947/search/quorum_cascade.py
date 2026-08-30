"""Exhaustive search over the Article I Section 5 quorum cascade, 1947 vantage.

STATUS: RESOLVED, and the answer is a null result. The write-up is
    ../quorum-cascade-null.md and the refutation is ../search/cascade_domination.py.
    The numbers below are correct and may be cited as what a cascade would do.
    They may NOT be cited as a threshold anyone can reach, for the reason below.

    The premise this file waited on turned out to be TRUE. The quorum base
    really is members chosen and sworn, not the statutory size of the chamber:
    Hinds' Precedents vol. 4 sections 2889 and 2891, verified from the page
    images in ../quorum-base.md. So a vacancy really does lower the denominator.

    The cascade fails anyway, on arithmetic that needed none of that research
    and that was sitting in this script's own output the whole time. Compare
    the two numbers main() already prints:

        two thirds of a quorum, settled 1920            : 179
        peak coalition required to get there            : 267

    Beginning the cascade costs a quorum of the undiminished chamber, because
    the bloc must supply that quorum itself; the members it is removing will not
    stay to help make one. And two thirds of a quorum is strictly fewer people
    than a quorum, for every chamber of four or more. So any bloc able to start
    this could already have proposed the amendment outright, 88 members ago.
    Strictly dominated at step 0. cascade_domination.py proves the general
    statement with Z3 and carries a negative control.

    One thing that bears on it and helps rather than hurts, kept for the record:
    Barry v. United States ex rel. Cunningham, 279 U.S. 597, 615-616 (1929),
    says in dictum that a vote of expulsion does not deprive a state of its
    equal suffrage in the constitutional sense. See academia/article-v-entrenchment.md.

Runs the row 4 -> row 5 linkage recorded in silence-inventory.md as an open
question, and turns it into a number.

THE MECHANISM UNDER TEST
    Article V's congressional threshold is two thirds of those present assuming
    a quorum (National Prohibition Cases, 253 U.S. 350 (1920)).
    A quorum is "a Majority of each" House (Art. I Sec. 5 cl. 1).
    The base of that majority is members chosen and sworn, not the statutory
    size of the chamber (House practice; United States v. Ballin, 144 U.S. 1
    (1892), which holds the House may fix by rule how a quorum is ascertained).
    Who is chosen and sworn is determined by the House itself, which is "the
    Judge of the Elections, Returns and Qualifications of its own Members"
    under the same clause.

    So the denominator of the Article V fraction is set by the body the
    fraction constrains. This file asks how far that can be driven.

THE TWO POWERS ARE NOT THE SAME PRICE, AND THAT ASYMMETRY IS THE POINT
    Exclusion of a member-elect is a judgment on qualifications under
    Art. I Sec. 5 cl. 1 and passed by SIMPLE MAJORITY of those voting.
    Expulsion of a sitting member requires "the Concurrence of two thirds"
    under Art. I Sec. 5 cl. 2.
    One clause, two adjacent sentences, and a supermajority guard on the
    second that is absent from the first.

VANTAGE DISCIPLINE
    December 5, 1947. Powell v. McCormack, 395 U.S. 486 (1969), which confines
    the Sec. 5 cl. 1 power to the standing qualifications of Art. I Sec. 2, is
    twenty-two years in the future and may not be used. At the vantage the
    governing practice is the other way: the House excluded Victor Berger in
    1919 and again in 1920 on grounds found nowhere in Art. I Sec. 2.

NOTHING HERE REACHES RATIFICATION. See the verdict printed at the end.
"""

import json
import math
from pathlib import Path

HOUSE_1947 = 435
SENATE_1947 = 96
STATES_1947 = 48


def quorum(sworn: int) -> int:
    """A Majority of each. Art. I Sec. 5 cl. 1."""
    return sworn // 2 + 1


def majority_of(present: int) -> int:
    """Simple majority of those voting. Exclusion, and ordinary business."""
    return present // 2 + 1


def two_thirds_of(present: int) -> int:
    """Two thirds of those present. Expulsion, and the Article V proposal."""
    return math.ceil(2 * present / 3)


def article_v_threshold(sworn: int) -> int:
    """Humans needed to carry an Article V proposal in a chamber of this size.

    Minimised over the number present, which the coalition controls: it wants
    exactly a quorum present and no more, because the fraction is taken of
    those present.
    """
    return two_thirds_of(quorum(sworn))


def cascade(start: int, label: str):
    """Exhaustively drive the chamber down and record every reachable state.

    Step 0 is exclusion at organisation of a new Congress, by simple majority.
    Every later step is expulsion of sitting members, at two thirds.

    At each step the acting bloc must (a) be large enough to supply the
    required vote with exactly a quorum present, and (b) still be seated
    afterwards. The search takes the largest legal cut at each stage and then
    verifies by exhaustion that no larger cut was available.
    """
    trace = []

    # ---- step 0: exclusion at organisation, simple majority ----
    # Members-elect present themselves; the base is the full chamber.
    q0 = quorum(start)
    # With only a quorum present, a simple majority of that quorum excludes.
    votes_to_exclude = majority_of(q0)
    # The bloc must be able to hold a quorum by itself once the rest are gone,
    # and must out-vote whoever attends. Adversarially, every non-member
    # attends, so the bloc needs a majority of the whole chamber.
    bloc_adversarial = majority_of(start)
    # If the opposition does not attend, the bloc must still supply a quorum.
    bloc_if_unopposed = q0
    bloc0 = min(bloc_adversarial, bloc_if_unopposed)

    sworn = bloc0  # everyone not in the bloc is excluded
    trace.append({
        "step": 0,
        "power": "exclusion, Art. I Sec. 5 cl. 1",
        "vote_rule": "simple majority of those voting, quorum present",
        "sworn_before": start,
        "quorum_before": q0,
        "bloc_required": bloc0,
        "votes_cast_required": votes_to_exclude,
        "sworn_after": sworn,
        "article_v_threshold_after": article_v_threshold(sworn),
    })

    # ---- steps 1..n: expulsion of sitting members, two thirds ----
    step = 1
    seen = {sworn}
    while True:
        q = quorum(sworn)
        need = two_thirds_of(q)          # votes to expel, quorum present
        # The expelling bloc must survive its own purge.
        survivors = need
        if survivors >= sworn:
            break                         # cannot cut further
        # Exhaustive check: is a deeper cut legal at this stage?
        best = None
        for target in range(1, sworn):
            if target < need:
                continue                  # bloc would not survive
            if need <= target < sworn:
                best = target if best is None else min(best, target)
        if best is None or best >= sworn or best in seen:
            break
        trace.append({
            "step": step,
            "power": "expulsion, Art. I Sec. 5 cl. 2",
            "vote_rule": "two thirds of those present, quorum present",
            "sworn_before": sworn,
            "quorum_before": q,
            "bloc_required": need,
            "votes_cast_required": need,
            "sworn_after": best,
            "article_v_threshold_after": article_v_threshold(best),
        })
        seen.add(best)
        sworn = best
        step += 1
        if step > 200:
            raise RuntimeError("cascade failed to terminate")

    return {
        "chamber": label,
        "statutory_size": start,
        "naive_two_thirds_of_membership": two_thirds_of(start),
        "threshold_before_cascade": article_v_threshold(start),
        "threshold_after_cascade": article_v_threshold(sworn),
        "final_sworn": sworn,
        "peak_coalition": max(t["bloc_required"] for t in trace),
        "steps": len(trace),
        "trace": trace,
    }


def main():
    out = {"vantage": "United States, December 5, 1947",
           "status": "NULL RESULT -- strictly dominated, see quorum-cascade-null.md",
           "premise_now_verified": ("the quorum base IS members chosen and sworn, per Hinds' "
                                    "Precedents vol. 4 ss. 2889 and 2891; see quorum-base.md"),
           "why_it_fails": ("beginning the cascade costs a quorum of the undiminished "
                            "chamber, and two thirds of a quorum is fewer people than a "
                            "quorum, so the manoeuvre is dominated at step 0"),
           "chambers": []}

    for start, label in ((HOUSE_1947, "House"), (SENATE_1947, "Senate")):
        r = cascade(start, label)
        out["chambers"].append(r)
        print(f"\n=== {label}, {start} seats ===")
        print(f"  'two thirds of both Houses' read as two thirds of the membership : "
              f"{r['naive_two_thirds_of_membership']}")
        print(f"  two thirds of a quorum, as settled in 1920                       : "
              f"{r['threshold_before_cascade']}")
        print(f"  after the cascade                                                : "
              f"{r['threshold_after_cascade']}")
        print(f"  final chamber size {r['final_sworn']}, "
              f"peak coalition {r['peak_coalition']}, {r['steps']} steps")
        for t in r["trace"]:
            print(f"    step {t['step']:>2}  {t['sworn_before']:>3} -> {t['sworn_after']:>3} sworn  "
                  f"| quorum {t['quorum_before']:>3} | needs {t['bloc_required']:>3} votes "
                  f"| Art V now {t['article_v_threshold_after']:>3}  ({t['power'].split(',')[0]})")

    house = out["chambers"][0]
    senate = out["chambers"][1]

    out["summary"] = {
        "naive_reading_total": (two_thirds_of(HOUSE_1947) + two_thirds_of(SENATE_1947)),
        "settled_1920_total": (article_v_threshold(HOUSE_1947) + article_v_threshold(SENATE_1947)),
        "after_cascade_total": (house["threshold_after_cascade"] + senate["threshold_after_cascade"]),
        "peak_coalition_total": house["peak_coalition"] + senate["peak_coalition"],
        "states_still_required_to_ratify": math.ceil(STATES_1947 * 3 / 4),
    }

    print("\n=== CONGRESSIONAL STAGE, BOTH CHAMBERS ===")
    s = out["summary"]
    print(f"  'two thirds of both Houses', read as membership : {s['naive_reading_total']}")
    print(f"  two thirds of a quorum, settled 1920            : {s['settled_1920_total']}")
    print(f"  after the Sec. 5 cascade                        : {s['after_cascade_total']}")
    print(f"  peak coalition required to get there            : {s['peak_coalition_total']}")

    print("\n=== VERDICT AGAINST method/what-counts-as-a-finding.md ===")
    print(f"  Article V still requires ratification by {s['states_still_required_to_ratify']} "
          f"of {STATES_1947} state legislatures.")
    print("  NOTHING IN THIS CASCADE TOUCHES THAT NUMBER.")
    print("  The cascade is confined to the proposing stage. It is not a path to")
    print("  amendment and therefore not a candidate. Recorded as a bounded result.")
    print(f"  AND IT IS DOMINATED: beginning it costs {s['peak_coalition_total']}, while proposing")
    print(f"  outright costs {s['settled_1920_total']}. See search/cascade_domination.py.")

    p = Path(__file__).with_name("quorum_cascade.json")
    p.write_text(json.dumps(out, indent=2))
    print(f"\n  wrote {p.name}")


if __name__ == "__main__":
    main()
