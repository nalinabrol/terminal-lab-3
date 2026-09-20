# Experiment Book 3

Tensor School | Introduction to Software Engineering

A 15-page, seven-experiment booklet covering **du, df, free, uptime, ps, top,
kill, zip, unzip and tar**. Keep Books 1 and 2 nearby for familiar file commands.

[Open the booklet](Experiment_Book_3.pdf) · [Editable Markdown](Experiment_Book_3.md)

[Create your Lab 3 Codespace](https://codespaces.new/nalinabrol/terminal-lab-3?quickstart=1)

Sign in with your own GitHub account and create on **main**. Wait for setup and
accept **Trust Folder & Continue** if prompted. A Bash terminal opens; if needed,
use **Lab 3: Focus Bash Terminal** in the Command Palette.

```bash
bash terminal-lab-3/start.sh
```

Enter your assigned ID, then run the exact `cd` command printed. Run `pwd` and
`cat identity.txt`. Follow the booklet from that lab root. Setup generates small,
deterministic practice files without downloading datasets. It preserves existing
attempts, including the earlier stage-1 format; use a new ID for the full book.

Keep `practice/`, `challenge/` and `identity.txt` unchanged. Save results in `work/`.
The process helper starts one bounded worker per attempt; follow the identity
checks before using `kill`. No broad process stopping is part of this lab.

Run the formative checker from your lab root:

```bash
python3 ../../terminal-lab-3/check.py
```

The full book has 35 checks. Explanations and interactive `top` use need instructor
review. The checker is read-only and does not submit anything. Save in nano with
Ctrl+O, Enter; Ctrl+X or F2 exits. Resume the same Codespace to retain progress.
Ignored `lab-work/` is not a GitHub backup; download work when a separate copy is needed.

## Source and validation

- `build_booklet.py` is the canonical editable authoring source. It generates the
  matching PDF and Markdown using Python and ReportLab. The checked-in PDF uses
  Arial/Courier on macOS; the builder falls back to DejaVu on Linux.
- `terminal-lab-3/` contains the practice-data generator, process helper and checker.
- `bash scripts/verify_environment.sh` runs the Linux validation suite in temporary
  attempts. It does not change student work. `verify_lab.py` and `verify_extra.py`
  are instructor validation tools, not student exercises.
- [Validation record](VALIDATION.md). Instructor answer guidance is distributed
  separately from the student booklet.

The earlier review draft is retained in Git history at
`fd24719b4c2f4cb5d14e52aeab7c24c6f71e5c95`.
