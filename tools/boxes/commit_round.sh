#!/bin/sh
# Commit the 2026-11-20 round in nix-lab, then the two docs in bunker. Run ON maximus.
set -e
cd /opt/src/nix-lab
git add research/local-gen/MODEL-NOTES.md research/local-gen/ROUND-2026-11-20-detail-and-order.md
git -c user.name=lead -c user.email=lead@cutestation commit -q -m "local-gen: H3 detail anchoring and depth order, round 2026-11-20

Name a small structured part and assert the shape holds; run the clip at the keyframe resolution
because a 512-wide take cannot keep a fine part; a nearest-to-furthest depth list fixes parts
landing on the wrong side. Model willingness probe: Krea 2 drops a hard detail entirely.
Also the queue-stuck workaround and the upload multipart finding."
git log --oneline -1

echo "--- bunker ---"
scp -q /tmp/bunker-commit.sh bunker:/tmp/bunker-commit.sh
ssh bunker sh /tmp/bunker-commit.sh
