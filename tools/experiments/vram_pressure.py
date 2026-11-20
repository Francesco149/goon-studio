#!/usr/bin/env python3
"""vram_pressure.py - hold a block of VRAM (and optionally RAM) to stand in for a browser.

A browser playing a 1080p/4K video, Discord with hardware acceleration, or a game launcher can
hold 0.5-2 GB of VRAM. This script reproduces that load on demand so the headroom flags can be
tested without depending on what happens to be open on the desktop.

  python tools/experiments/vram_pressure.py --vram 1.5 --hold 600
  python tools/experiments/vram_pressure.py --vram 1.5 --ram 2 --delay 20 --hold 120

--delay waits before allocating (to grab memory in the middle of a job, like opening a tab).
Run it with the engine's embedded python (it needs torch with CUDA). Ctrl+C or --hold ends it.
"""
import argparse
import time

import torch


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--vram", type=float, default=1.5, help="GB of VRAM to hold")
    ap.add_argument("--ram", type=float, default=0.0, help="GB of system RAM to hold")
    ap.add_argument("--delay", type=float, default=0.0, help="seconds to wait before allocating")
    ap.add_argument("--hold", type=float, default=600.0, help="seconds to hold, then exit")
    a = ap.parse_args()

    time.sleep(a.delay)
    blocks = []
    if a.vram > 0:
        n = int(a.vram * (1 << 30))
        t = torch.empty(n, dtype=torch.uint8, device="cuda")
        t.fill_(1)  # touch it so the driver really commits the pages
        blocks.append(t)
    if a.ram > 0:
        r = bytearray(int(a.ram * (1 << 30)))
        for i in range(0, len(r), 4096):
            r[i] = 1
        blocks.append(r)
    torch.cuda.synchronize() if a.vram > 0 else None
    print("holding %.2f GB VRAM, %.2f GB RAM for %ds" % (a.vram, a.ram, a.hold), flush=True)
    try:
        time.sleep(a.hold)
    except KeyboardInterrupt:
        pass


if __name__ == "__main__":
    main()
