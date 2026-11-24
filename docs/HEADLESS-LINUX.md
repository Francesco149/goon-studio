# Goon Studio on a headless Linux server

**Not part of the normal setup.** The Studio is built for the user's own Windows PC (`kit\setup.ps1`,
AGENTS.md section 1a). This page is for one case only: the user **asks** to run it on a headless Linux
machine they reach over their LAN (a home server with a bigger GPU). An agent does not offer it
otherwise.

What runs there: the engine (ComfyUI at the version in `kit/engine.json`) and the Studio page, as two
services. The user opens the page from any browser on the LAN; the pictures stay on the server.

## Install

```sh
git clone https://github.com/Francesco149/goon-studio && cd goon-studio
kit/linux/setup.sh --data /srv/goon          # engine + models under /srv/goon, pictures in ./gallery
```

`kit/linux/setup.sh` (safe to run again):

- finds the card (`nvidia-smi`, or `/dev/kfd` for AMD ROCm; `--gpu nvidia|amd` to force it);
- clones ComfyUI at the pinned version, makes a venv with PyTorch for the card (CUDA 13 wheels, or the
  ROCm wheels), adds ComfyUI-GGUF (the only custom node the workflows use) and PyAV;
- writes `my/settings.json` (`comfy_url` 127.0.0.1:8187, `engine_dir`, `models_dir` =
  `<data>/models`, `headless: true`) and wires the engine to the store (`store.py wire`);
- installs two **systemd user units**, `goon-engine` (ComfyUI on 127.0.0.1 only) and `goon-studio`
  (the page on `--host 0.0.0.0`, port 8191), and enables lingering so they run without a login.

Options: `--host 127.0.0.1` keeps the page local too (reach it through an SSH tunnel:
`ssh -L 8191:127.0.0.1:8191 server`), `--engine-port`, `--page-port`, `--flags "..."` (engine launch
flags; the defaults are the measured ones below), `--no-services`, `--dry-run` (print what it would do).

Then the models, as on Windows: `<data>/engine/.venv/bin/python tools/models/store.py fetch anime_pov egirl`
(AGENTS.md 1a step 5; Civitai files need the key, section 4c). Files the user already has on another
machine can be copied into `<data>/models/<folder>/` under the same names.

## Running it

| | |
|---|---|
| page | `http://<server>:8191` (`--host` decides who can reach it) |
| engine | `127.0.0.1:8187` on the server; the page talks to it, the browser never does |
| services | `systemctl --user status goon-engine goon-studio`, logs with `journalctl --user -u goon-engine` |
| update | `git pull` in the checkout, then `systemctl --user restart goon-studio` |
| flags | edit `ExecStart` in `~/.config/systemd/user/goon-engine.service` (or rerun setup with `--flags`) |

**The page has no login.** Anyone who can reach port 8191 sees the gallery, including the private
pictures, and can queue jobs. Keep it on a trusted LAN or behind the SSH tunnel; never forward the
port to the internet.

## An agent working with a headless install

The page and the gallery live on the server. An agent on another machine renders through the engine
(open port 8187 to that machine only, or tunnel it) with `--engine http://<server>:8187` on
`tools/rounds/run_template_round.py` / `run_story.py`, and every result is pulled into **its own**
checkout's `gallery/<round>/` over HTTP, so nothing has to be copied by hand. The page's own (private)
pictures stay on the server and stay private: the same gate as on Windows (AGENTS.md section 1).
`tools/boxes.local.json` (git-ignored, `tools/localboxes.py`) can name the server and make it the tools'
default with `"_default"`.

## Performance

8 GB cards: `docs/PERFORMANCE-8GB.md`. 16 GB and up (the measured Linux pass was on a 16 GB AMD card
with ROCm): `docs/PERFORMANCE-16GB.md`. On AMD keep `--reserve-vram 1.5`: the measured 16 GB card
corrupts output when VRAM runs nearly full.

## NixOS

The setup script assumes an FHS distribution (pip wheels link against `/usr/lib`). On NixOS, wrap the
engine in a `buildFHSEnv` (Python 3.13, `uv`, git, gcc, glibc, zlib, libGL, the X client libs for
OpenCV, ffmpeg) and run the same two services from it; the author's own setup is a NixOS module
of that shape, kept outside this repo.
