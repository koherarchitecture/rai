#!/usr/bin/env bash
# Every check rai must pass before a change lands. The contract test is the one that must never fail:
# it is what programs built on rai rely on (GUIDELINE.md). Run from the repository root:
#   bash scripts/check.sh            # uses .venv/bin/python if present, else PYTHON, else python3
#   PYTHON=/path/to/python bash scripts/check.sh
set -u
cd "$(dirname "$0")/.."
P="${PYTHON:-}"; [ -n "$P" ] || { for c in .venv/bin/python "$HOME/.local/share/rai/.venv/bin/python" python3; do [ -x "$c" ] || command -v "$c" >/dev/null 2>&1 || continue; P=$c; break; done; }
"$P" -c 'import torch, transformers, yaml' 2>/dev/null || { echo "$P cannot import torch, transformers and pyyaml — make the virtual environment first (see the README), or set PYTHON"; exit 1; }
fail=0
run () {   # run <name> <script> [args]
  printf '\n— %s\n' "$1"; shift
  out=$("$P" "$@" 2>&1); st=$?          # status of the script itself, never of a pipe: a check that cannot fail is not a check
  printf '%s\n' "$out" | grep -v -E 'Loading weights|^Warning|unauthenticated'
  [ "$st" -eq 0 ] || { fail=1; printf '  FAILED (exit %s)\n' "$st"; }
}
run "the contract programs built on rai rely on" tests/test_contract.py
run "the tally" tests/test_tally.py
run "the trained reader on test set v1" tests/test_reader_v03.py
printf '\n— no training row repeats a test set\n'
"$P" - <<'PY' || fail=1
import json, glob, os
norm = lambda s: s.strip().lower().rstrip(".")
held = {norm(json.loads(l)["answer"]) for t in glob.glob("tests/testset*.jsonl") for l in open(t)}
rows = [json.loads(l) for l in open("data/train-synth.jsonl")]
leaks = [r for r in rows if norm(r["answer"]) in held or (r["span"] and norm(r["span"]) in held)]
print(f"  {len(rows)} training rows, {len(held)} held-out answers, {len(leaks)} repeats")
assert not leaks, f"{len(leaks)} training rows repeat a test set, e.g. {leaks[0]['answer']!r}"
PY
printf '\n'; [ "$fail" -eq 0 ] && echo "all checks passed" || { echo "SOMETHING FAILED — the change does not land"; exit 1; }
