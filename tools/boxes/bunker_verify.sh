#!/bin/bash
cd /opt/src/bunker || exit 1
echo "worktree:"; wc -l docs/SEX-SCENES.md; head -3 docs/SEX-SCENES.md; tail -4 docs/SEX-SCENES.md
echo "HEAD version:"; git show HEAD:docs/SEX-SCENES.md | wc -l
echo "diff stat:"; git show --stat --oneline HEAD | head -6
