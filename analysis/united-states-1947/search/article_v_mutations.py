"""Plant four specific defects in disposable copies and require the tests to fail."""

import json
from pathlib import Path
import shutil
import subprocess
import sys
import tempfile


HERE = Path(__file__).resolve().parent
MUTATIONS = (
    (
        "ratification-threshold-bypass",
        "if len(support.ratifiers) < state.constitution.ratifiers_required:",
        "if False:",
        "test_35_states_cannot_ratify_or_bootstrap_a_lower_threshold",
    ),
    (
        "consent-count-instead-of-identity",
        "if not deprived <= support.consenters:",
        "if len(deprived) > len(support.consenters):",
        "test_consent_identity_not_just_cardinality",
    ),
    (
        "same-instrument-self-authorization",
        "if before.proviso:",
        "if after.proviso:",
        "test_same_instrument_cannot_use_its_own_repeal",
    ),
    (
        "proposal-changes-law-without-ratification",
        "return State(state.constitution, step.amendment)",
        "return State(amended(state.constitution, step.amendment, support.states), step.amendment)",
        "test_proposal_has_no_normative_effect",
    ),
)


def main():
    source = (HERE / "article_v_model.py").read_text(encoding="utf-8")
    controls = []
    for name, old, new, test in MUTATIONS:
        if source.count(old) != 1:
            raise RuntimeError(f"{name}: mutation anchor must occur exactly once")
        with tempfile.TemporaryDirectory(prefix="godel-article-v-mutation-") as directory:
            work = Path(directory)
            for filename in ("article_v_model.py", "article_v_smt.py", "test_article_v.py"):
                shutil.copy2(HERE / filename, work / filename)
            command = [
                sys.executable, "-B", "-m", "unittest", f"test_article_v.ArticleVTests.{test}",
            ]
            baseline = subprocess.run(
                command, cwd=work, capture_output=True, text=True, timeout=60, check=False,
            )
            if baseline.returncode != 0:
                raise RuntimeError(
                    f"{name}: unmutated control failed; interpreter={sys.executable}; "
                    f"prefix={sys.prefix}\n{baseline.stderr}"
                )
            (work / "article_v_model.py").write_text(source.replace(old, new), encoding="utf-8")
            mutant = subprocess.run(
                command, cwd=work, capture_output=True, text=True, timeout=60, check=False,
            )
            caught = (
                mutant.returncode == 1
                and "FAIL:" in mutant.stderr
                and "FAILED (failures=" in mutant.stderr
            )
            controls.append({
                "defect": name,
                "unmutated_exit": baseline.returncode,
                "mutated_exit": mutant.returncode,
                "behavioral_assertion_caught_defect": caught,
            })
            if not caught:
                print(mutant.stdout + mutant.stderr, file=sys.stderr)
    print(json.dumps({"mutation_controls": controls}, indent=2))
    return 0 if all(control["behavioral_assertion_caught_defect"] for control in controls) else 1


if __name__ == "__main__":
    raise SystemExit(main())
