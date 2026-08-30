# Tooling

This file covers what is installed, how to check that it works, and what was expensive to figure out. It is not procedure and not analysis, so it lives here rather than in `method/` or `analysis/`.

The governing rule is that a tool is not usable in this project until it has re-derived a result someone else has published. That is `method/README.md`'s validation rule applied to borrowed machinery: a citation asserts that the machinery works, and we cannot inspect machinery from a citation. Everything below is either validated in that sense or explicitly marked as not.

## Checking it

```
./verify.sh
```

Twenty-five checks, exit 0 when all pass. Five of them are **negative controls**, which the harness scores as passing only when they fail: a solver asked for an unsatisfiable model, a Prolog query that is false, a theory asserting `1 + 1 = 3`, and countermodel searches that must succeed. A harness that can only print PASS cannot tell a working toolchain from a broken assertion. If a control reports `CONTROL BROKEN`, disbelieve every other line.

Section 6 of the output lists what is deliberately *not* verified. Read it before quoting any number from the rest.

Cloned repositories and downloaded PDFs are scratch and untracked. The harness reads them from `GL_WORK`, defaulting to `/tmp/gl-replication`, and prints checksums so a fresh copy can be compared against ours.

## What is installed

| Tool | Version | Validated by |
|---|---|---|
| Z3 | 5.1.0, in `.venv/` | re-derived the 146 / 33 / 36 thresholds independently |
| SWI-Prolog | 10.0.2, Homebrew | full replication of the IRC §121 model below |
| Isabelle/HOL | 2025-2 | proves the US-1947 constitutional theory; rejects a false one |
| Lean 4 | 4.33.1, elan | **nothing.** Version string only; no Lean has been written |

Lean is listed so that its status is unambiguous. LegalLean is the reason it is installed and remains untried.

## Isabelle, the hard way

Several hours went into this and none of it is discoverable from the documentation.

The Homebrew cask is broken. It registers `Isabelle2025-2.app`, links `/opt/homebrew/bin/isabelle`, and installs no files, leaving a dangling symlink that presents as a successful install.

The documented download host redirects to a port that is not reachable. The redirect target refuses HTTPS without a token, and `HEAD` returns 403 even when the token is supplied, so probe with a range `GET`. The URL that works:

```
https://dist.isabelle.cit.tum.de/dist/Isabelle2025-2_macos.tar.gz?token=Isabelle
```

That is 1,730,395,791 bytes, SHA-256 `8f187496e295f169952e944745af9e4ae00c9c1cd2ed4cadbcf7d898e444913e`, confirmed identical across two independent downloads. No official checksum is published, so this figure is ours and carries only the authority of having been derived twice.

Clear quarantine with `xattr -dr com.apple.quarantine` before moving into `/Applications`. Gatekeeper blocks the bundled jEdit GUI but not the command line, so do not launch it from Finder. The HOL heap ships prebuilt and there is no long first build.

`isabelle process` no longer exists in this release. The invocation is:

```
isabelle process_theories -O -U -f X.thy X
```

## The technique validation

**Yadamsuren, Platt & Diaz, IRC §121.** Cited in `academia/formal-methods.md`; upstream commit `501cf03487e74b1f2057b73c066e9ce8fa13f6ed`.

This one validates a method rather than a document, so it has no home in `analysis/`: it would not change if you swapped countries, and it examines a tax statute rather than any constitution. What it tests is the pipeline this project expects to depend on — a language model used only as a translator into a symbolic representation, with a solver doing the actual checking.

The Prolog appendices replicate completely on local SWI-Prolog. A fully-qualified couple returns `no_divergence`; an asymmetric couple returns `divergence` at $375,000 against $250,000; output is byte-identical across three runs; and the CLP(FD) phase recovers the $10,416 gap. The paper used SWISH rather than a local install, so this is a genuine external replication rather than a re-run of their environment.

What does not replicate is the number the bibliography leaned on hardest. Their repository holds only the three Prolog appendices — no benchmark set, no harness, no accuracy data. The claim that a model alone detects inconsistencies about a third of the time while the hybrid reaches full accuracy cannot be checked from the published artifacts. It may be true; it is not verifiable, and `academia/formal-methods.md` now says so rather than citing the figure flat.

The transferable finding is the weaker but checkable one: the symbolic half is deterministic and reproduces exactly, which is the property the pipeline is chosen for.

## The correspondence problem

The most instructive failure here was not a tool being wrong. It was a tool being right about a formula that did not say what its label claimed. The incident is written up where it happened, in `analysis/united-states-1947/formal-model-replication.md`, in the file whose main result is a successful machine-checked proof, because that is where the caution is most needed. It is not restated here; the numbers live in one place so they cannot drift.

The general rule is the part that belongs in this file. Every tool in the table above is exposed to this failure and none of them checks for it. A verified result is only as good as the correspondence between the formula and the sentence attached to it, and that correspondence is the one link no prover inspects.

The harness committed the same error against itself, which is the better illustration because it was caught by running rather than by reading. The two consistency lemmas were written without an explicit Nitpick timeout, so under load the model finder hit its default and gave up. The harness read the absence of a countermodel as a result and printed `could not refute False -- axiom set is inconsistent`. That is wrong twice: a timeout is not a negative answer, and even a genuine failure to find a countermodel would not establish inconsistency, only that none was found within the bound. The check failed roughly one run in six, which is worse than failing always, because an intermittent alarm trains the reader to ignore it.

Both halves are fixed. The lemmas now carry `timeout = 300`, and the harness distinguishes three outcomes rather than two: `PASS`, `FAIL`, and `INCONCLUSIVE` for when a tool returns no answer at all. Six consecutive clean runs followed. The general rule this yields is worth more than the fix — any check built on a search procedure needs a third outcome, because searches that do not terminate are the normal case and reporting them as refutations manufactures findings.

The rule needed widening once. A later experiment raised the number of concurrent Nitpick calls in one theory from four to seven, and one lemma came back with `Malformed Kodkodi output: ill-formed Kodkodi output` instead of a verdict. That is not a timeout, so the timeout-only detection classified it as a failed check — the exact error the three-valued scheme was introduced to prevent, reappearing because the list of ways a tool can decline to answer was written from the one instance then in hand. The detector now also matches malformed solver output and Nitpick's own failure message. A search procedure has more failure modes than running out of time, and enumerating them from a single observed example will under-count them.
