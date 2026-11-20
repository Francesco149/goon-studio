#!/bin/sh
# Undo the 2026-11-20 doc commit in bunker.
set -e
cd /opt/src/bunker
git config --global --add safe.directory /opt/src/bunker 2>/dev/null || true
git -c safe.directory=/opt/src/bunker reset --mixed HEAD~1
git -c safe.directory=/opt/src/bunker checkout -- docs/STYLE-LOCK.md
rm -f docs/SEX-SCENES.md docs/NSFW-RESEARCH.md
echo "bunker now:"
git -c safe.directory=/opt/src/bunker status --short | cat
git -c safe.directory=/opt/src/bunker log --oneline -1 | cat
