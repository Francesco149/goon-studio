#!/bin/bash
set -x
systemctl stop lame-comfyui
pkill -f comfyui-fhs 2>/dev/null
sleep 3
sed -e 's/--reserve-vram 1.5/--reserve-vram 0.5 --lowvram/' \
    /nix/store/c11qvw1v9vz9k0azg7xi8ws12xndmx55-comfyui-launch \
    > /lamedata/comfyui/my-launch.sh
chmod +x /lamedata/comfyui/my-launch.sh
grep exec -A2 /lamedata/comfyui/my-launch.sh
nohup /nix/store/2lnbb8iymxjk456axdjjpkl1ha4d1prd-comfyui-fhs/bin/comfyui-fhs /lamedata/comfyui/my-launch.sh > /lamedata/comfyui/lowvram.log 2>&1 &
sleep 25
curl -s -o /dev/null -w "http %{http_code}\n" http://127.0.0.1:8188/system_stats
tail -5 /lamedata/comfyui/lowvram.log
