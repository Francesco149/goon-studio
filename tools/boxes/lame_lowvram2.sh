#!/bin/bash
set -x
systemctl stop lame-comfyui 2>/dev/null
systemctl stop lame-comfy-low 2>/dev/null
pkill -f comfyui-fhs 2>/dev/null
sleep 3
systemd-run --unit=lame-comfy-low --collect --service-type=simple \
  /nix/store/2lnbb8iymxjk456axdjjpkl1ha4d1prd-comfyui-fhs/bin/comfyui-fhs /lamedata/comfyui/my-launch.sh
sleep 25
systemctl is-active lame-comfy-low
curl -s -o /dev/null -w "http %{http_code}\n" http://127.0.0.1:8188/system_stats
journalctl -u lame-comfy-low --no-pager | tail -8
