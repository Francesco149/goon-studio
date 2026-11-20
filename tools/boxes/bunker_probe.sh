#!/bin/bash
cd /opt/src/bunker || exit 1
rm -f docs/_t.txt
git remote -v
git branch --show-current
git config user.name
git config user.email
git status --short | head -10
