#!/usr/bin/env bash
# Download the H3 act LoRAs and Pink Alchemy Anima into a ComfyUI models folder. Resumable; skips
# files already there.  Usage: bash tools/models/dl_h3.sh "<engine_dir>/ComfyUI/models"
set -u
M="${1:?usage: dl_h3.sh <ComfyUI models dir>}"
mkdir -p "$M/loras/h3nsfw" "$M/unet"
dl() { # url dest
  local url="$1" dest="$2"
  if [ -s "$dest" ]; then
    echo "have $(basename "$dest") $(stat -c%s "$dest")"
    return
  fi
  echo "get $(basename "$dest")"
  curl -L --retry 8 --retry-delay 3 -C - -o "$dest" "$url" || echo "FAIL $dest"
}
B=https://huggingface.co/kimjob/h3_NSFW_lora/resolve/main/loras/H3
dl "$B/prod/HMNSFW_AIO_V2.safetensors" "$M/loras/h3nsfw/HMNSFW_AIO_V2.safetensors"
dl "$B/prod/MM-H3%20-%20Blowjob.safetensors" "$M/loras/h3nsfw/MM-H3-Blwjob.safetensors"
dl "$B/test/MM-H3%20-%20Blowjob%20v3.safetensors" "$M/loras/h3nsfw/MM-H3-Blwjob-v3.safetensors"
dl "$B/test/HMCumshot_V2.safetensors" "$M/loras/h3nsfw/HMCumshot_V2.safetensors"
dl "$B/test/H3_Motion_BoosterV2.safetensors" "$M/loras/h3nsfw/H3_Motion_BoosterV2.safetensors"
dl "$B/test/Minimax3_BoobPhysics_v1.safetensors" "$M/loras/h3nsfw/Minimax3_BoobPhysics_v1.safetensors"
dl "$B/test/zy_Amateur_Pov_H3.safetensors" "$M/loras/h3nsfw/zy_Amateur_Pov_H3.safetensors"
dl "$B/test/Titjob%20-%20Titfuck%20ComfyTinker%20Minimax%20V0.9safetensors.safetensors" "$M/loras/h3nsfw/Titjob-Titfuck-H3.safetensors"
dl "$B/test/h3-sideview-deepthroat-step00007800-k3nk.safetensors" "$M/loras/h3nsfw/h3-sideview-deepthroat.safetensors"
dl "$B/test/HMPenis_v2_e35.safetensors" "$M/loras/h3nsfw/HMPenis_v2_e35.safetensors"
dl "$B/test/blowjob_in_cheek_101_h3_.safetensors" "$M/loras/h3nsfw/blowjob_in_cheek.safetensors"
dl "https://huggingface.co/RunningHubAI/rh-minimax-h3-astro-nsfw-lora/resolve/main/Astro%20nsfw.safetensors" "$M/loras/h3nsfw/Astro-nsfw.safetensors"
dl "https://huggingface.co/RunningHubAI/rh-ramthrusts-nsfw-pink-alchemy-anima-v2.9-unet/resolve/main/ramthrustsNSFWPINK_v29Anima10base.safetensors" "$M/unet/ramthrustsNSFWPINK_v29.safetensors"
echo ALLDONE
