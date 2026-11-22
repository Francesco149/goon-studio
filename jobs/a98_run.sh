#!/bin/sh
# round a98: re-anchoring variants on two known-bad clips (docs/ANIME-TIMING.md)
PY=/f/LLStudioTest/engine/ComfyUI_windows_portable/python_embeded/python.exe
E=http://10.0.10.240:8188
cd "$(dirname "$0")/.."
for m in selfguide repair; do
  $PY tools/rounds/reanchor.py jobs/a98_reanchor.jsonl pz_short a98 --mode $m --pass1 gallery/a97/lz_g_pz_close_96101_00001_.mp4 --engine $E
  $PY tools/rounds/reanchor.py jobs/a98_reanchor.jsonl bj_profile a98 --mode $m --pass1 gallery/a97/lz_v_bj_profile_00001_.mp4 --engine $E
done
$PY tools/rounds/reanchor.py jobs/a98_reanchor.jsonl bj_profile a98 --mode ref2va --engine $E
echo a98 done
