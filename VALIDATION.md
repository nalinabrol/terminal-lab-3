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

The container explicitly installs procps, zip, unzip and tar. Live Codespace and
clean rebuild results will be recorded after checking this published version.
Local tests alone are not Codespace verification.

Limits: formative file checks do not prove independent work or evaluate written
explanations. Interactive top and nano need live observation. Container memory
readings need not match the Codespace resource limit. No fixed PIDs, capacity,
free-space readings or memory values are required.
