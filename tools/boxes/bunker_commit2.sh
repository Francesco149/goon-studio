#!/bin/bash
set -x
ls -ld /opt/src/bunker /opt/src/bunker/docs || exit 1
cp /tmp/SEX-SCENES.md /opt/src/bunker/docs/SEX-SCENES.md || exit 2
cp /tmp/SEX-SCENES-2.md /opt/src/bunker/docs/SEX-SCENES-2.md || exit 3
ls -l /opt/src/bunker/docs/SEX-SCENES.md /opt/src/bunker/docs/SEX-SCENES-2.md || exit 4
cd /opt/src/bunker || exit 5
git add docs/SEX-SCENES.md docs/SEX-SCENES-2.md || exit 6
git -c user.name=headpats -c user.email=headpats@bunker.local commit -m "docs: session 2 explicit-scene recipes (e-girl, Pink Alchemy, H3 act LoRAs, restyle)" || exit 7
git log --oneline -2
git status --short | head -5
