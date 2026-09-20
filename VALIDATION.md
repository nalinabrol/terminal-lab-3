# Experiment 1 verification - 21 September 2026 (IST)

This is a verified **review draft through Experiment 1**, not the completed Book 3.

## Published runtime and fresh Codespace

- Verified runtime/configuration revision: `ed29f90e33fe7b10f04a4e3cd2f63a8390da2f77`.
- A genuinely new Codespace was created from that published revision:
  `musical-space-zebra-x9x57qqx5ggf6x44`.
- [Owner's review Codespace](https://musical-space-zebra-x9x57qqx5ggf6x44.github.dev/).
  This requires the owning account; it is not a student sharing link.
- [Student launch link](https://codespaces.new/nalinabrol/terminal-lab-3?quickstart=1).
- Live OS: Ubuntu 24.04.3 LTS; GNU coreutils 9.4; nano 7.2.

The first diagnostic Codespace exposed a startup-order issue: the editor server was
not yet present during postCreate. Installation of the terminal extension was moved
to postAttach. The second fresh Codespace installed it successfully, hid sidebars
and maximized the terminal without manual installation. The first Codespace was
stopped after diagnosis, not deleted.

## Live student workflow

A new `REVIEW-E1` attempt was created interactively with `bash terminal-lab-3/start.sh`.
The printed absolute path, identity and directory structure were checked. Every
Experiment 1 shell command was run through the browser terminal, including guided
measurements, snapshots, the copy sequence and the independent application.

- Unfinished attempt: 1/9 checks; originals passed, all eight unfinished results
  were flagged with feedback.
- Completed attempt: **9/9 file checks passed**.
- Observation fields edited/saved in nano and reopened to verify persistence.
- Setup rerun with the same ID: all **16 files** matched their before-rerun SHA-256
  hashes. Before-copy evidence and completed results were retained.
- Each of the six original binary payloads on `/workspaces` had allocated blocks
  accounting for its full logical length; no sparse payloads.
- Folder usage grew after the copy while the rounded filesystem row stayed the
  same. The draft requires observations, not fixed capacity/free-space values.

## Automated correct/incorrect-result checks

`bash scripts/verify_environment.sh` passed locally in Linux, in GitHub Actions,
and in the fresh live Codespace. Temporary attempts for `A017`, `B104`, `C233` and
`student-42` each passed 9/9, with targeted failures for every checker item.

Also verified: missing reports, extra/changed originals, a symlink instead of a
copy, read-only checker behaviour, setup preservation, six invalid ID formats,
full payload allocation, and resistance to compression. Tests use isolated
temporary attempts and do not modify student work.

[Successful CI for the verified runtime](https://github.com/nalinabrol/terminal-lab-3/actions/runs/35537790918).

## Artifacts and limits

Seven A4 PDF pages were rendered and visually checked. Page totals, review-draft
labels and the clickable Codespaces URL were verified. Published Markdown/PDF
were checked against local files through unauthenticated public downloads.

Browser automation intercepted injected Ctrl+X in nano. Ctrl+O and Enter saved
correctly; **F2 exited successfully**. The booklet includes this fallback. A
physical-keyboard Ctrl+X test across student browsers is not claimed.

The checker validates saved evidence, not understanding, provenance or independent
work. Explanations require instructor review. The repo exposes setup/checker/test
source because this is practice. Instructor answer notes are not in the student
booklet. No real student data, credentials or unrelated course files were published.

The final draft update adds the tested nano fallback and this verification record;
runtime/configuration are unchanged from the fresh-Codespace revision above.
