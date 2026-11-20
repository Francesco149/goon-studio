#!/bin/bash
set -x
cd /opt/src/bunker || exit 1
cp /tmp/SEX-SCENES-3.md docs/SEX-SCENES-3.md || exit 2
printf '\n## See also\n\n- `docs/SEX-SCENES-3.md` - session 3: owner verdicts, the facial/cum-shot recipe, the anime motion recipe.\n' >> docs/SEX-SCENES-2.md
git add docs/SEX-SCENES-2.md docs/SEX-SCENES-3.md || exit 3
git -c user.name=headpats -c user.email=headpats@bunker.local commit -m "docs: session 3 explicit scenes (facial/cum-shot recipe, anime motion, owner verdicts)" || exit 4
git log --oneline -2
git status --short | head -5
