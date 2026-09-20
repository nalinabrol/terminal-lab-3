#!/usr/bin/env bash
set -euo pipefail
lab_kit="$(cd -- "$(dirname -- "${BASH_SOURCE[0]}")" && pwd)"
for lab_command in bash python3 nano du df cp cat ls; do
    command -v "$lab_command" >/dev/null || { printf 'Missing command: %s\n' "$lab_command" >&2; exit 1; }
done
python3 -B "$lab_kit/setup.py"
