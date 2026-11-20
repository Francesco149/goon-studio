#!/bin/sh
# Run ON bunker: install the approved explicit-scene recipe doc and link it from STYLE-LOCK.md.
set -e
cd /opt/src/bunker
git config --global --add safe.directory /opt/src/bunker 2>/dev/null || true
cp /tmp/SEX-SCENES.md docs/SEX-SCENES.md
if ! grep -q "SEX-SCENES.md" docs/STYLE-LOCK.md; then
  printf '\n## Explicit scenes\n\nThe recipes for explicit scenes that are approved (erotic anime faces and poses, correct photoreal\nstills, blowjob motion in a clip) and the ones still open (anime cock anatomy, photoreal video\nanatomy, cum), each marked with its status: `docs/SEX-SCENES.md`. Renders, prompts and seeds behind\nevery claim: `~/goonlab` on cutestation.\n' >> docs/STYLE-LOCK.md
fi
OWNER=$(stat -c %U /opt/src/bunker)
chown "$OWNER" docs/SEX-SCENES.md docs/STYLE-LOCK.md
git -c safe.directory=/opt/src/bunker add docs/SEX-SCENES.md docs/STYLE-LOCK.md
git -c safe.directory=/opt/src/bunker -c user.name=lead -c user.email=lead@cutestation commit -q -m "docs: explicit scene recipes, approved and open, 2026-11-20

Approved by the owner and written up here: erotic anime faces and poses (two prompts kept verbatim,
only the cock half varies), correct cocks in photoreal stills (Krea 2 Turbo + the Verite realism
LoRA, act-then-him-then-his-cock prompt shape, strength 1.0-1.3), and blowjob motion in a clip with
its variations (stroke duration, the lip seal, the held bottom, scripted sound, first+last frame
anchoring, Ref2VA, head-only work, and what not to do).

Marked incomplete on purpose: anime cock anatomy (hit or miss; Anima Base beats Aesthetic, weighted
part tags, censored variants work as presentation not as a fix, and the next step needs a download
decision), photoreal video anatomy (the glans deforms under suction unless the exit state is pinned
as an image), and cum (glue in motion)."
git -c safe.directory=/opt/src/bunker log --oneline -2
