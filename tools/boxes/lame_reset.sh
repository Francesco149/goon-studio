#!/bin/bash
echo "== before"
ps -eo pid,rss,cmd | grep -i comfy | grep -v grep | head -5
cat /sys/class/drm/card*/device/mem_info_vram_used 2>/dev/null
systemctl stop lame-comfyui 2>/dev/null
pkill -f comfyui-fhs 2>/dev/null
sleep 3
systemctl start lame-comfyui
sleep 12
systemctl is-active lame-comfyui
ps -eo pid,rss,cmd | grep -i comfy | grep -v grep | head -5
cat /sys/class/drm/card*/device/mem_info_vram_used 2>/dev/null
curl -s -o /dev/null -w "http %{http_code}\n" http://127.0.0.1:8188/system_stats
