#!/bin/bash
cd /lamedata/comfyui || exit 1
./.venv/bin/python - <<'PY'
import torch
print("torch", torch.__version__, "cuda", torch.cuda.is_available())
if torch.cuda.is_available():
    print(torch.cuda.get_device_name(0))
PY
