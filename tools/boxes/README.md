# tools/boxes: author-only

These scripts drive the repo author's own lab machines (ampere, lame, maximus, bunker, nixlab).
Those machines exist only on the author's home network. **On any other install, do not run
anything in this folder, do not look for those hosts, and do not adapt these scripts to reach
other machines.** A normal install has one engine: the local ComfyUI that `kit\start.ps1` runs
(127.0.0.1:8188, `--box local`).

They are kept for the author's sessions, which also have the git-ignored `AGENTS.local.md`.
