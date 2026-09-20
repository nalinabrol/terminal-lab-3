#!/usr/bin/env bash
set -euo pipefail
lab_repository="$(cd -- "$(dirname -- "${BASH_SOURCE[0]}")/.." && pwd)"
cd "$lab_repository"
for lab_command in bash python3 nano du df free uptime ps top kill zip unzip tar cp cat ls diff; do
    command -v "$lab_command" >/dev/null || { printf 'Missing: %s\n' "$lab_command" >&2; exit 1; }
done
du --version | head -n 1
df --version | head -n 1
bash -n terminal-lab-3/start.sh
python3 -B verify_lab.py
printf '\nLab 3 seven-experiment environment is ready.\n'
printf 'Start: bash terminal-lab-3/start.sh\n'
