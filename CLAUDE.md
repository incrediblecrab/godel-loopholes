# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) and GitHub Copilot CLI when working in this repository.

This repository studies whether the US constitutional order in force in 1947 permitted a lawful sequence of actions that destroys democratic government, and whether that illuminates Kurt Gödel's reported citizenship-exam concern. It has not found a verified loophole or identified Gödel's argument; the substantive search is paused and instrument work continues. The repository is public, and `site/` publishes it to GitHub Pages. Start from `analysis/united-states-1947/research-report.md`; `eli5.md` is the general-audience introduction.

## Commands

```bash
python3 tools/facts.py --check      # every value in data/facts.json is present in the file it names as owner
python3 tools/contrast.py --check
python3 tools/links.py --check      # every path a file points at exists; without --check it exits 0 on a dangle
python3 tools/ssot_audit.py         # lists every file a load-bearing value appears in
./verify.sh                         # toolchain and replication harness (Z3, SWI-Prolog, Isabelle), with negative controls
cd site && npm run build            # lockfile, fact and token lints, astro check, build, CSP seal and check
```

`.github/workflows/pages.yml` runs the fact, contrast and SSOT checks, regenerates `data/ablation.json` from `analysis/united-states-1947/search/axiom_sweep.py inventory` and fails if the committed copy differs, builds the site and runs the browser check; it triggers on changes to `site/`, `data/`, `analysis/`, `tools/`, `eli5.md`, `README.md` and a few others. `TOOLING.md` records installed tool versions and the non-obvious Isabelle setup (`isabelle process_theories`, not `isabelle process`); `./verify.sh` reads downloaded sources from `GL_WORK` (default `/tmp/gl-replication`). In `verify.sh`, a negative control passes only by failing, and a "CONTROL BROKEN" line invalidates every other line.

## Rules

Facts are single-sourced: every number in `data/facts.json` names one owning file, and narrative in other files may reword but not restate a different value; change the owner and the JSON together, then run `tools/facts.py --check`. A file that moves prose elsewhere leaves a pointer, which `tools/links.py` checks. A proposed loophole counts only if it meets `method/what-counts-as-a-finding.md` (authorized steps, an explicit coalition, a concrete falsifier), and instrument results follow `method/what-counts-as-an-instrument-result.md`; keep negative and corrected results in the record. A tool is usable here only after it has re-derived a published result (`method/README.md`). Primary legal texts live in `corpus/`; downloaded papers and cloned repositories stay untracked.

`.githooks/pre-push` refuses a `site/package-lock.json` that would not install on Linux CI; this clone sets `core.hooksPath` to `.githooks`, so it runs on every push here; a fresh clone needs `git config core.hooksPath .githooks`.
