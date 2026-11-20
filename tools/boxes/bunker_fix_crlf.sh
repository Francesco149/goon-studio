#!/bin/bash
cd /opt/src/bunker || exit 1
file docs/SEX-SCENES.md docs/SEX-SCENES-2.md
git config core.autocrlf || echo "autocrlf unset"
python3 - <<'PY'
p="docs/SEX-SCENES.md"
b=open(p,"rb").read()
print("crlf", b.count(b"\r\n"), "lf", b.count(b"\n"))
open(p,"wb").write(b.replace(b"\r\n", b"\n"))
PY
file docs/SEX-SCENES.md
git add docs/SEX-SCENES.md
git -c user.name=headpats -c user.email=headpats@bunker.local commit --amend -m "docs: session 2 explicit-scene recipes (e-girl, Pink Alchemy, H3 act LoRAs, restyle)"
git show --stat --oneline HEAD | head -6
git log --oneline -2
