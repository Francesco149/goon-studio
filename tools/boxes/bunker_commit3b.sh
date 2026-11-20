#!/bin/bash
set -x
cd /opt/src/bunker || exit 1
cp /tmp/SEX-SCENES-3.md docs/SEX-SCENES-3.md || exit 2
git add docs/SEX-SCENES-3.md || exit 3
git -c user.name=headpats -c user.email=headpats@bunker.local commit -m "docs: session 3 addendum (cum material vs dynamics, twitch spec)" || exit 4
git log --oneline -2
