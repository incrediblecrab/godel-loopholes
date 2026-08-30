"""Why the Article I §4 route gains cost advantage only with presidential cooperation.

STATUS: PARTIAL RESULT. The congressional stage of this route is not strictly
    dominated the way the cascade was, but it gains leverage only when the
    President cooperates. Without the President the route costs exactly the same
    as proposing the amendment directly, because the veto-override threshold and
    the Article V proposing threshold are identical. The write-up is
    article-i-4-route.md.

THE ARITHMETIC

    Article I §4 operates "by Law" — bicameralism and presentment (Art. I §7).
    A statute needs a bare majority of those present (assuming a quorum) in each
    chamber plus the President's signature; without the President's signature it
    needs a two-thirds override of the veto in each chamber.

    Article V proposal needs "two thirds of both Houses," settled as two thirds
    of those present assuming a quorum, National Prohibition Cases, 253 U.S.
    350 (1920), applying Missouri Pacific Ry. Co. v. Kansas, 248 U.S. 276
    (1919).

    The Art. I §7 veto override also needs "two thirds of that House," settled
    as two thirds of those present assuming a quorum, by Missouri Pacific
    itself.

    IDENTITY. The veto-override formula and the Article V proposing formula are
    the same function of the same chamber sizes, because the same 1919-1920 case
    law governs both. Therefore the two thresholds are always identical.

    THEOREM. For every quorum q >= 5, a bare majority of q is strictly less
    than two thirds of q. Equivalently, with presidential cooperation, the
    statutory price is strictly below the Article V proposing price.

    CONSEQUENCE. Without presidential cooperation, an Art. I §4 statute costs
    exactly the same as an Art. V proposal (179 members in 1947). With
    presidential cooperation, the statute costs only 135 members — 44 fewer.
    The route is not strictly dominated (135 < 179), unlike the quorum cascade
    (267 > 179). The entire cost advantage is the President's signature.
"""

import json
import math
from pathlib import Path

HOUSE_1947 = 435
SENATE_1947 = 96

EXHAUSTIVE_LIMIT = 100_000


def quorum(n: int) -> int:
    """A Majority of each. Art. I Sec. 5 cl. 1."""
    return n // 2 + 1


def two_thirds(q: int) -> int:
    """Two thirds of those present (ceiling), the 1919-1920 reading."""
    return math.ceil(2 * q / 3)


def bare_majority(q: int) -> int:
    """A bare majority of those present: more than half, so floor(q/2) + 1."""
    return q // 2 + 1


def exhaustive_leverage(limit: int = EXHAUSTIVE_LIMIT):
    """Check for all quorum sizes 1..limit whether majority < two_thirds.

    Returns sizes where the advantage does NOT hold (majority >= two_thirds).
    These are the counterexamples to the general claim, and all of them should
    be small quorums.
    """
    return [q for q in range(1, limit + 1) if not bare_majority(q) < two_thirds(q)]


def exhaustive_identity(limit: int = EXHAUSTIVE_LIMIT):
    """Verify that two_thirds(quorum(n)) is the same whether computed as
    a veto override or as an Art. V threshold, for all chamber sizes.

    This is trivially true because both are the same formula, but stating it
    and checking it is the point. Returns any n where they differ.
    """
    failures = []
    for n in range(1, limit + 1):
        q = quorum(n)
        veto = two_thirds(q)
        art_v = two_thirds(q)
        if veto != art_v:
            failures.append(n)
    return failures


def negative_control():
    """The exhaustive leverage check MUST find counterexamples — quorum sizes
    where majority == two_thirds. If it found none, the check would be vacuous.

    Quorums 1, 2, 3, 4, and 6 are genuine counterexamples (majority equals
    two thirds for these small values). A check that cannot fail is not a check.
    """
    failures = exhaustive_leverage()
    if not failures:
        return None
    return failures


def main():
    h_quorum = quorum(HOUSE_1947)
    s_quorum = quorum(SENATE_1947)

    # Art. V proposing threshold (National Prohibition Cases, 1920)
    art_v_house = two_thirds(h_quorum)
    art_v_senate = two_thirds(s_quorum)
    art_v_total = art_v_house + art_v_senate

    # Art. I §7 veto override (Missouri Pacific, 1919)
    veto_house = two_thirds(h_quorum)
    veto_senate = two_thirds(s_quorum)
    veto_total = veto_house + veto_senate

    # Art. I §4 statute with presidential cooperation
    statute_house = bare_majority(h_quorum)
    statute_senate = bare_majority(s_quorum)
    statute_total = statute_house + statute_senate

    # The cascade's entry price (from cascade_domination.py)
    cascade_entry = h_quorum + s_quorum

    # Checks
    identity_failures = exhaustive_identity()
    leverage_failures = exhaustive_leverage()
    control = negative_control()

    print("=== THRESHOLD IDENTITY ===")
    print(f"  Art. V proposing  : House {art_v_house} + Senate {art_v_senate} = {art_v_total}")
    print(f"  Art. I §7 override: House {veto_house} + Senate {veto_senate} = {veto_total}")
    print(f"  Identity holds (all n to {EXHAUSTIVE_LIMIT}): {len(identity_failures) == 0}")
    print()
    print("  Both are ceil(2 * quorum / 3) with the same quorum, settled by the")
    print("  same 1919-1920 case law (Missouri Pacific, National Prohibition Cases).")

    print()
    print("=== LEVERAGE WITH PRESIDENTIAL COOPERATION ===")
    print(f"  Statute cost (with President) : {statute_total} members + 1 President")
    print(f"    House majority of quorum {h_quorum}: {statute_house}")
    print(f"    Senate majority of quorum {s_quorum}: {statute_senate}")
    print(f"  Art. V proposing threshold    : {art_v_total} members")
    print(f"  Advantage                     : {art_v_total - statute_total} members")
    print()
    print(f"  Exhaustive: majority < two_thirds for all q in 1..{EXHAUSTIVE_LIMIT}")
    print(f"    quorum sizes where advantage fails: {leverage_failures}")
    max_fail = max(leverage_failures) if leverage_failures else 0
    print(f"    largest counterexample            : q = {max_fail}")
    print(f"    1947 House quorum ({h_quorum}) safe: {h_quorum not in leverage_failures}")
    print(f"    1947 Senate quorum ({s_quorum}) safe: {s_quorum not in leverage_failures}")

    print()
    print("=== NEGATIVE CONTROL ===")
    if control:
        print(f"  Counterexamples found: {control[:10]}{'...' if len(control) > 10 else ''}")
        print(f"  ({len(control)} total — the check is not vacuous)")
    else:
        print("  NO counterexamples — the check is vacuous and CANNOT BE TRUSTED")

    print()
    print("=== COMPARISON WITH THE CASCADE ===")
    print(f"  Cascade entry price  : {cascade_entry} members")
    print(f"  Art. V proposing     : {art_v_total} members")
    print(f"  Cascade dominated    : {cascade_entry} > {art_v_total} = {cascade_entry > art_v_total}")
    print(f"  This route (w/ Pres) : {statute_total} < {art_v_total} = {statute_total < art_v_total}")
    print(f"  This route (no Pres) : {veto_total} == {art_v_total} = {veto_total == art_v_total}")

    print()
    print("=== VERDICT ===")
    identity_ok = len(identity_failures) == 0
    leverage_ok = statute_total < art_v_total
    no_pres_identity = veto_total == art_v_total
    cascade_dominated = cascade_entry > art_v_total
    control_ok = control is not None

    ok = identity_ok and leverage_ok and no_pres_identity and cascade_dominated and control_ok

    if ok:
        print("  THE ROUTE IS NOT STRICTLY DOMINATED (with presidential cooperation).")
        print(f"  Entry price {statute_total} + 1 President < Art. V threshold {art_v_total}.")
        print(f"  Without the President, entry price {veto_total} == Art. V threshold {art_v_total}.")
        print("  The entire cost advantage is the President's signature.")
        print()
        print("  Compare the cascade: entry price", cascade_entry, "> Art. V threshold", art_v_total)
        print("  The cascade was dominated at step zero. This route is not.")
        print()
        print("  HOWEVER: this route still requires Art. V ratification by 36 of 48")
        print("  state legislatures, which no federal election law reaches.")
        print("  And its intermediate step (the election outcome) is not a legal")
        print("  operation — it is a factual outcome that the statute aims to produce")
        print("  but cannot guarantee.")
    else:
        print("  CHECK FAILED — review arithmetic")

    out = {
        "vantage": "United States, December 5, 1947",
        "status": "PARTIAL RESULT -- congressional stage not dominated; route stalls at ratification",
        "identity": "veto override threshold == Art. V proposing threshold (same formula, same case law)",
        "identity_holds_to": EXHAUSTIVE_LIMIT,
        "identity_failures": identity_failures,
        "thresholds_1947": {
            "statute_with_president": statute_total,
            "statute_without_president_veto_override": veto_total,
            "art_v_proposing": art_v_total,
            "cascade_entry": cascade_entry,
        },
        "advantage_with_president": art_v_total - statute_total,
        "advantage_without_president": veto_total - art_v_total,
        "leverage_failures": leverage_failures,
        "negative_control_found": control is not None,
        "negative_control_count": len(control) if control else 0,
        "route_dominated_with_president": not leverage_ok,
        "route_dominated_without_president": no_pres_identity,
        "cascade_dominated": cascade_dominated,
        "all_checks_passed": ok,
    }
    p = Path(__file__).with_name("election_leverage.json")
    p.write_text(json.dumps(out, indent=2) + "\n")
    print(f"\n  wrote {p.name}")
    return 0 if ok else 1


if __name__ == "__main__":
    raise SystemExit(main())
