# Experiment Book 3 validation

The complete booklet contains 15 pages and seven experiments. The canonical
builder emits matching PDF/Markdown, with the real student launch URL visibly
printed and clickable on page 1. Every page was rendered and visually inspected.

Local Ubuntu 24.04 validation passed for A017, B104, C233 and student-42:

- Correct work: 35/35 checks for each ID.
- All 35 targeted incorrect-evidence cases rejected; additional missing-report,
  extra/altered-original and symlink-as-copy cases rejected.
- Incomplete ZIP and plain tar renamed as gzip rejected; timeout does not count as
  SIGTERM. Extraction checks compare actual bytes, including nested members.
- Checker leaves attempt bytes unchanged; setup reruns preserve them.
- Worker start reruns reuse the live PID; stopped workers are not replaced.
- Deterministic payloads are allocated, not sparse; binary storage payloads resist
  compression. Repeated text compresses much more than the supplied noise.
- Invalid IDs rejected. Legacy identities retain their original nine-check scope.

The container explicitly installs procps, zip, unzip and tar. Both a live clean rebuild and fresh Codespace creation were verified below.

Limits: formative file checks do not prove independent work or evaluate written
explanations. Interactive top and nano need live observation. Container memory
readings need not match the Codespace resource limit. No fixed PIDs, capacity,
free-space readings or memory values are required.

## Live verification - 21 September 2026 (IST)

The container configuration was tested through **Full Rebuild** in the existing
[musical space zebra review Codespace](https://musical-space-zebra-x9x57qqx5ggf6x44.github.dev/).
The clean build and postCreate suite completed successfully. Its editor connection
stalled afterwards; stopping/resuming restored it. All 16 saved REVIEW-E1 hashes
still matched and that preserved attempt passed 9/9 with the updated checker.

The booklet's exact student launch link was also used to create a new 2-core
[studious giggle Codespace](https://studious-giggle-x9x57qqxwx4hq7x.github.dev/).
It cloned `ed0a18092733aa84db00e552dca09d9c4a3afd26`. Its postCreate suite passed,
and postAttach installed the terminal startup extension and maximized Bash.
The fresh student attempt is `/workspaces/terminal-lab-3/lab-work/lab3-REVIEW-FULL`.

All seven experiments were exercised through the browser terminal, including
nano edits, Ctrl+O/Enter saves, F2 exit, live top refreshes, Shift+P/Shift+M sorting,
q exit, filtered top, a fresh PID/token check, SIGTERM and header-only ps afterwards.
Both ZIP handovers and tar recovery matched original bytes. Student commands used
observed PIDs and readings; none are fixed answer requirements.

The live run exposed whitespace padding in uptime's elapsed-time field. Revision
`8446e79952be40523309e3528aef33a8b7270d77` trims display padding and adds a regression
case. The complete suite passed again inside the fresh Codespace on that revision:
four IDs, each 35/35 plus all targeted incorrect-work cases. CI also
[passed on that revision](https://github.com/nalinabrol/terminal-lab-3/actions/runs/35540018607).
Container configuration did not change after the clean build/creation.

- REVIEW-FULL: initial 1/35; completed 35/35.
- Moving its guided ZIP aside produced the expected CHECK; restoring it returned
  the checker to 35/35. Incorrect feedback is saved in the attempt.
- Same-ID setup rerun and a separate read-only checker run both preserved all
  **58** attempt file hashes. An invalid `../invalid` ID was rejected.
- Repeated worker start reused the same live PID; after kill it reported STOPPED.
- Tracked trees were clean and student evidence was confirmed ignored by Git.
- All 150 existing Lab 1-2 course assets matched their original hash baseline.

Both review Codespaces require their owner's GitHub account. Other students use
[the launch link](https://codespaces.new/nalinabrol/terminal-lab-3?quickstart=1).
