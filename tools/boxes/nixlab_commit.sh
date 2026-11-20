#!/bin/bash
set -x
cd /opt/src/nix-lab || exit 1
cp /tmp/nixlab-round-2.md research/local-gen/ROUND-2026-11-20-egirl-and-restyle.md || exit 2
git add research/local-gen/ROUND-2026-11-20-egirl-and-restyle.md || exit 3
git -c user.name=headpats -c user.email=cute@headpats.uk commit -m "local-gen: round 2026-11-20 overnight (nvfp4 load, act-LoRA A/B, per-frame restyle)" || exit 4
git log --oneline -2
git status --short | head -5
