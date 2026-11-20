#!/bin/bash
echo "== processes"
ps -eo pid,rss,cmd | grep -iE 'comfyui|main.py' | grep -v grep | cut -c1-160
echo "== vram bytes"
cat /sys/class/drm/card*/device/mem_info_vram_used 2>/dev/null
echo "== total"
cat /sys/class/drm/card*/device/mem_info_vram_total 2>/dev/null
echo "== unit"
systemctl is-active lame-comfy-low
journalctl -u lame-comfy-low --no-pager | tail -5
