#!/usr/bin/env bash
# kit/linux/setup.sh - Goon Studio on a headless Linux server (engine + page as systemd user services).
#
# Not part of the normal setup (that is kit\setup.ps1 on the user's Windows PC). Use this only when the
# user asks for the Studio on a headless Linux box they reach over the LAN; docs/HEADLESS-LINUX.md.
#
#   kit/linux/setup.sh --data /srv/goon [--gpu nvidia|amd] [--host 0.0.0.0] [--engine-port 8187]
#                      [--page-port 8191] [--flags "..."] [--profile16] [--no-services] [--dry-run]
#
# Installs, under --data: engine/ (ComfyUI at kit/engine.json's version, a Python venv with PyTorch for
# the card, the ComfyUI-GGUF node) and models/ (the store; tools/models/store.py fetches into it).
# Writes my/settings.json (gallery in this checkout's gallery/ unless it already says otherwise) and
# two systemd *user* units: goon-engine (ComfyUI) and goon-studio (the page, --host on the LAN).
# Safe to run again. Needs: git, python3 (3.12 or 3.13) with venv, ffmpeg, curl; the GPU driver
# (NVIDIA >= 580 for CUDA 13, or ROCm-capable amdgpu).
set -euo pipefail

REPO=$(cd "$(dirname "$0")/../.." && pwd)
DATA="" GPU="" HOST="0.0.0.0" EPORT=8187 PPORT=8191 FLAGS="" SERVICES=1 DRY=0 PROFILE=""
while [ $# -gt 0 ]; do
  case "$1" in
    --data) DATA=$2; shift 2 ;;
    --gpu) GPU=$2; shift 2 ;;
    --host) HOST=$2; shift 2 ;;
    --engine-port) EPORT=$2; shift 2 ;;
    --page-port) PPORT=$2; shift 2 ;;
    --flags) FLAGS=$2; shift 2 ;;
    --no-services) SERVICES=0; shift ;;
    --profile16) PROFILE=16gb; shift ;;   # 16 GB+ card, the user said yes: keep an 8 GB card's headroom (docs/PERFORMANCE-16GB.md)
    --dry-run) DRY=1; shift ;;
    -h|--help) sed -n '2,16p' "$0" | sed 's/^# \{0,1\}//'; exit 0 ;;
    *) echo "unknown option $1" >&2; exit 2 ;;
  esac
done
[ -n "$DATA" ] || { echo "--data <folder> is required (engine + models, ~25-130 GB; an SSD)" >&2; exit 2; }
say() { echo "[goon-setup] $*"; }
run() { if [ "$DRY" = 1 ]; then echo "+ $*"; else "$@"; fi; }

# ---------------------------------------------------------------- 1. the card
VRAM_GB=""
if [ -z "$GPU" ]; then
  if command -v nvidia-smi >/dev/null && nvidia-smi -L >/dev/null 2>&1; then GPU=nvidia
  elif [ -e /dev/kfd ]; then GPU=amd
  else echo "no NVIDIA (nvidia-smi) or AMD ROCm (/dev/kfd) GPU found; pass --gpu" >&2; exit 12; fi
fi
if [ "$GPU" = nvidia ]; then
  VRAM_GB=$(nvidia-smi --query-gpu=memory.total --format=csv,noheader,nounits | head -1 | awk '{printf "%.1f", $1/1024}')
else   # AMD: the biggest card's VRAM from sysfs (a second, smaller card may sit beside it)
  VRAM_GB=$(cat /sys/class/drm/card*/device/mem_info_vram_total 2>/dev/null | sort -n | tail -1 | awk '{printf "%.1f", $1/1073741824}')
fi
say "GPU: $GPU, VRAM: ${VRAM_GB:-?} GB"

# kit/engine.json pins the ComfyUI version the Windows build ships; PyTorch per card
VERSION=$(python3 -c "import json;print(json.load(open('$REPO/kit/engine.json',encoding='utf-8-sig'))['engine']['version'])")
case "$GPU" in
  nvidia) TORCH_INDEX=https://download.pytorch.org/whl/cu130 ;;
  amd) TORCH_INDEX=https://download.pytorch.org/whl/rocm7.14 ;;   # AMD's own wheels (repo.amd.com) are also fine
  *) echo "--gpu must be nvidia or amd" >&2; exit 2 ;;
esac
# the measured defaults: docs/PERFORMANCE-8GB.md (8 GB, NVIDIA) and docs/PERFORMANCE-16GB.md (16 GB+)
if [ -z "$FLAGS" ]; then
  FLAGS="--use-ck-attention"
  [ "$GPU" = nvidia ] && FLAGS="$FLAGS --fast fp16_accumulation"
  [ "$GPU" = amd ] && FLAGS="--reserve-vram 1.5 $FLAGS"
fi

# the 16 GB profile: the engine keeps an 8 GB card's headroom, the rest of the card stays free
if [ "$PROFILE" = 16gb ] && [ -n "$VRAM_GB" ]; then
  FLAGS="$(echo "$FLAGS" | sed -E 's/--reserve-vram [0-9.]+//') --reserve-vram $(awk "BEGIN{printf \"%.1f\", $VRAM_GB - 7.5}")"
fi

# ---------------------------------------------------------------- 2. engine
ENGINE="$DATA/engine"
run mkdir -p "$ENGINE" "$DATA/models"
if [ ! -d "$ENGINE/ComfyUI/.git" ]; then
  run git clone --filter=blob:none https://github.com/comfyanonymous/ComfyUI "$ENGINE/ComfyUI"
fi
run git -C "$ENGINE/ComfyUI" fetch --tags --quiet origin
run git -C "$ENGINE/ComfyUI" checkout --quiet --detach "$VERSION"
[ -x "$ENGINE/.venv/bin/python" ] || run python3 -m venv "$ENGINE/.venv"
PY="$ENGINE/.venv/bin/python"
run "$PY" -m pip install --quiet --upgrade pip
run "$PY" -m pip install --quiet torch torchvision torchaudio --index-url "$TORCH_INDEX"
run "$PY" -m pip install --quiet -r "$ENGINE/ComfyUI/requirements.txt"
# the one custom node the workflows use (UnetLoaderGGUF); the maintained fork, pinned
GGUF="$ENGINE/ComfyUI/custom_nodes/ComfyUI-GGUF"
[ -d "$GGUF/.git" ] || run git clone --filter=blob:none https://github.com/molbal/ComfyUI-GGUF "$GGUF"
run git -C "$GGUF" checkout --quiet --detach da5f435cd9a9e54ad27eed417ed72b1f2543ef41
run "$PY" -m pip install --quiet -r "$GGUF/requirements.txt"
run "$PY" -m pip install --quiet av   # the page's "use the last frame" (ffmpeg is the fallback)
if [ "$DRY" = 0 ]; then
  "$PY" -c "import torch;ok=torch.cuda.is_available();print('torch',torch.__version__,'gpu',torch.cuda.get_device_name(0) if ok else 'NOT VISIBLE');raise SystemExit(0 if ok else 1)" \
    || { echo "PyTorch does not see the GPU (driver / ROCm version?)" >&2; exit 14; }
fi

# ---------------------------------------------------------------- 3. settings + the store
GALLERY="$REPO/gallery"
if [ "$DRY" = 0 ]; then
  mkdir -p "$REPO/my" "$GALLERY/outputs" "$GALLERY/inputs"
  python3 - "$REPO/my/settings.json" "$EPORT" "$ENGINE" "$DATA/models" "$GALLERY" "$FLAGS" "$GPU" "${VRAM_GB:-0}" "$PROFILE" <<'PY'
import json, sys
path, port, engine, models, gallery, flags, gpu, vram, profile = sys.argv[1:]
try:
    s = json.load(open(path, encoding="utf-8-sig"))
except (OSError, ValueError):
    s = {}
s.update({"comfy_url": "http://127.0.0.1:%s" % port, "engine_dir": engine, "models_dir": models,
          "extra_flags": flags, "gpu": gpu, "vram_gb": float(vram or 0), "headless": True})
s.setdefault("data_dir", gallery)
if profile:
    s["perf_profile"] = profile
json.dump(s, open(path, "w", encoding="utf-8"), indent=2)
print("settings:", path)
PY
  "$PY" "$REPO/tools/models/store.py" wire
fi
GALLERY=$(python3 -c "import json;print(json.load(open('$REPO/my/settings.json'))['data_dir'])" 2>/dev/null || echo "$GALLERY")

# ---------------------------------------------------------------- 4. services (systemd --user)
if [ "$SERVICES" = 1 ]; then
  UNITS="$HOME/.config/systemd/user"
  run mkdir -p "$UNITS"
  ENGINE_UNIT="[Unit]
Description=Goon Studio engine (ComfyUI $VERSION)
After=network-online.target

[Service]
WorkingDirectory=$ENGINE/ComfyUI
ExecStart=$PY main.py --listen 127.0.0.1 --port $EPORT --output-directory $GALLERY/outputs --input-directory $GALLERY/inputs --database-url sqlite:///$GALLERY/engine.db --disable-auto-launch --preview-method none $FLAGS
Restart=on-failure
RestartSec=10

[Install]
WantedBy=default.target"
  PAGE_UNIT="[Unit]
Description=Goon Studio page
After=goon-engine.service

[Service]
WorkingDirectory=$REPO/kit/studio
ExecStart=$PY server.py --engine http://127.0.0.1:$EPORT --port $PPORT --host $HOST
Restart=on-failure
RestartSec=10

[Install]
WantedBy=default.target"
  if [ "$DRY" = 1 ]; then echo "$ENGINE_UNIT"; echo; echo "$PAGE_UNIT"
  else
    printf '%s\n' "$ENGINE_UNIT" > "$UNITS/goon-engine.service"
    printf '%s\n' "$PAGE_UNIT" > "$UNITS/goon-studio.service"
    systemctl --user daemon-reload
    systemctl --user enable --now goon-engine.service goon-studio.service
    # keep them running without a login session
    loginctl enable-linger "$USER" 2>/dev/null || say "run 'sudo loginctl enable-linger $USER' so the services survive logout"
  fi
fi
say "done. Page: http://$(hostname -I 2>/dev/null | awk '{print $1}'):$PPORT (engine stays on 127.0.0.1:$EPORT)."
say "Next: models, e.g. $PY $REPO/tools/models/store.py fetch anime_pov egirl (AGENTS.md 1a step 5)."
if [ -n "$VRAM_GB" ] && awk "BEGIN{exit !($VRAM_GB >= 15.5)}"; then
  if [ -z "$PROFILE" ]; then say "16 GB+ card: the 16 GB profile is available (docs/PERFORMANCE-16GB.md): rerun with --profile16 if the user wants it."; fi
fi
