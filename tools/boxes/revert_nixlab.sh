#!/bin/sh
# Undo the 2026-11-20 doc commits in nix-lab. Leaves every OTHER uncommitted change alone
# (results.jsonl and the voice-eval files belong to another session).
set -e
cd /opt/src/nix-lab
git reset --mixed HEAD~1
git checkout -- research/local-gen/MODEL-NOTES.md
rm -f research/local-gen/ROUND-2026-11-20-detail-and-order.md
echo "nix-lab now:"
git status --short | cat
git log --oneline -1 | cat
