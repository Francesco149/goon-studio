#!/bin/sh
# Run ON bunker: commit the two new docs plus the cross-link. Never touches anything else.
set -e
cd /opt/src/bunker
git config --global --add safe.directory /opt/src/bunker 2>/dev/null || true
if ! grep -q "SEX-SCENES.md" docs/STYLE-LOCK.md; then
  printf '\n## Explicit scenes\n\nHow the lab builds an explicit scene that stays well formed - the shot grammar, the keyframe and\nclip recipes, what each model will and will not draw, and the anchors for anatomy and cum:\n`docs/SEX-SCENES.md`. The survey of the field LoRAs that fix anatomy is `docs/NSFW-RESEARCH.md`.\n' >> docs/STYLE-LOCK.md
fi
OWNER=$(stat -c %U /opt/src/bunker)
chown -R "$OWNER" docs/SEX-SCENES.md docs/NSFW-RESEARCH.md docs/STYLE-LOCK.md
git -c safe.directory=/opt/src/bunker add docs/SEX-SCENES.md docs/NSFW-RESEARCH.md docs/STYLE-LOCK.md
git -c safe.directory=/opt/src/bunker -c user.name=lead -c user.email=lead@cutestation commit -q -m "docs: explicit scene recipe and the NSFW LoRA survey, 2026-11-20

SEX-SCENES.md: the three failure shapes on H3 video and what fixes each, which image model draws
explicit anatomy, the two compositions that work, the prompt words that backfire, mosaic as post,
and the LoRA route the field actually uses. NSFW-RESEARCH.md: the LoRAs that target our bases,
including one for MiniMax H3 itself."
git -c safe.directory=/opt/src/bunker log --oneline -3
