# Experiment Book 3 - Review Draft through Experiment 1

Tensor School | Introduction to Software Engineering

**Stage 1 only:** opening/setup and Experiment 1, using `du` and `df`.
The rest of Book 3 is awaiting review and is not included.

[Create your Lab 3 Codespace](https://codespaces.new/nalinabrol/terminal-lab-3?quickstart=1)

This is a public course repository. Sign in with your own GitHub account and create
on `main`; subsequently resume that same Codespace. Wait for setup to finish.
Accept **Trust Folder & Continue** if asked. A Bash terminal opens; if needed use
**Lab 3: Focus Bash Terminal** in the Command Palette.

```bash
bash terminal-lab-3/start.sh
```

Enter your assigned lab ID (not an email), run the exact `cd` command printed, then
`pwd` and `cat identity.txt`. Follow the booklet. Setup creates `lab-work/lab3-ID`
and preserves every file on a rerun. Keep original evidence unchanged and save
results in `work/`. Generated attempts are ignored by Git and are not uploaded.

- [Student booklet PDF](Experiment_Book_3_Review_Draft.pdf): seven A4 pages.
- [Editable Markdown source](Experiment_Book_3_Review_Draft.md).
- [Layout and content builder](build_booklet.py): canonical authoring source,
  generates the PDF and Markdown together. Python + ReportLab; Arial on macOS,
  DejaVu on Linux. Edit this file to keep both outputs synchronized.
- [Verification evidence](VALIDATION.md).

## Experiment 1

Measure supplied event folders, compare human-readable units, inspect the filesystem
containing the lab folder, and distinguish usage from available capacity. Make one
working copy, preserve before/after evidence, then apply the commands independently
to three magazine-team folders. No fixed free-space numbers are assumed.

The setup creates about 13.1 MiB of deterministic, fully written synthetic binary
exports. They stand in for stored media and documents; they are not playable files.
No downloads, credentials, or real student data are used. All practice data is
provided reproducibly by `terminal-lab-3/setup.py`.

From your lab root, check saved files:

```bash
python3 ../../terminal-lab-3/check.py
```

Nine read-only feedback checks validate originals, measurements, folder choices,
filesystem field transcription and the copy. They do not repair or submit files,
and cannot assess explanations or prove independent work. Source is visible because
this is practice, not a secure assessment. Instructor answers are kept out of the
student booklet.

## Maintainer validation

```bash
bash scripts/verify_environment.sh
```

Requires Linux with GNU coreutils, Bash, Python 3 and nano. This uses temporary
attempts, never existing student work. It tests four IDs, correct/incorrect results,
missing/altered evidence, deterministic payload allocation and setup preservation.
The Codespace uses Ubuntu 24.04 and the same check on creation. GitHub Actions also
runs it. The devcontainer's terminal defaults follow Books 1-2; settings can be
changed by students.

Command semantics: [GNU du](https://www.gnu.org/software/coreutils/manual/html_node/du-invocation.html)
and [GNU df](https://www.gnu.org/software/coreutils/manual/html_node/df-invocation.html).
