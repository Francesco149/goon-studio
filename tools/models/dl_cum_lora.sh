#!/usr/bin/env bash
set -u
M=/data/comfyui/models/loras/h3nsfw
B=https://huggingface.co/kimjob/h3_NSFW_lora/resolve/main/loras/H3
dl() { curl -fsSL --retry 5 -C - -o "$M/$2" "$1" && echo "ok $2 $(stat -c%s "$M/$2")" || echo "FAIL $2"; }
dl "$B/test/epic_cumshots-MiniMaxH3-ALPHA-CUMSH0T.safetensors" "epic_cumshots.safetensors"
dl "$B/prod/CUMOUF_oral_creampie_H3_v1.safetensors" "CUMOUF_creampie.safetensors"
dl "$B/test/MH3_Cum_05b.safetensors" "MH3_Cum_05b.safetensors"
dl "$B/test/HMCumshot_V1.0.safetensors" "HMCumshot_V1.safetensors"
echo DONE
