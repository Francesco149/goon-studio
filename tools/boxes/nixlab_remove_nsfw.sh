#!/bin/bash
set -x
cd /opt/src/nix-lab || exit 1
git log --oneline -3
git status --short | head -5
git reset --mixed bf38355 || exit 2
rm -f research/local-gen/ROUND-2026-11-20-egirl-and-restyle.md
git log --oneline -2
git status --short | head -8
git push --force-with-lease origin master || exit 3
git log --oneline -2
