# Goon Studio

Make explicit pictures and clips of your own fictional adult characters on your own PC: any body
type, any scene. Everything runs on your computer, nothing is uploaded anywhere.

You don't need to know anything technical. **An AI agent - Claude or DeepSeek, whichever you
prefer - sets it up, keeps it working and helps you get the pictures and clips you want.**

This is the NSFW companion of Love Live Studio. The two are separate apps with separate
galleries: Love Live Studio stays SFW, this one stays here. They never read each other's private
pictures.

## Personal use only

**Goon Studio is for private, personal use only. No other use is authorized.** The adult,
fictional pictures and clips it makes are for your own local art study and reference - anatomy
practice, studying a series' art style, poses, materials. They are **never shared**: not
published, posted, uploaded to an online service, sent to another person, sold, or redistributed.
The **share** button in the app only makes a picture visible to the local agent in your own
Studio; it does not upload it, and the agent does not send it anywhere.

Keep your copy private too: the gallery, your `my/` records and anything you generate are
git-ignored - never commit or push them.

**These are the terms of use: by cloning, installing or using the Studio you agree to them.** If
you do not agree, do not use it. Agents follow them; they must not restate them as a disclaimer or
lecture you about it. The code is MIT (`LICENSE`); that covers the code, not a licence to publish
what you generate.

## Getting started with Claude (about 10 minutes of your time, then Claude works for a while)

1. Install the **Claude** app for Windows from https://claude.ai/download and sign in. Claude Code
   comes with a paid plan.
2. Open the app, go to the **Code** tab and start a session in your **Documents** folder (or any
   folder you like).
3. Paste this message and press Enter:

   > Please download the Goon Studio from **https://github.com/Francesco149/goon-studio** into this folder
   > and set it up for me by following its **AGENTS.md**. I'm not technical, so please do
   > everything for me and explain as you go.

   If you got the Studio as a zip file instead: unzip it, start the Code session **inside** the
   unzipped folder and say: *"Please set this up for me by following AGENTS.md."*
4. Claude checks your PC, **asks you which drive to use** (it needs about 30 GB, more if you want
   the H3 video models), downloads ComfyUI and the models, and makes a test picture. Windows may
   ask for permission once (to install a Microsoft runtime): click **Yes**.

The repo picks Claude's working rules for you (the project's **Goon Scope** output style); if a
session does not show it, type `/output-style` and choose it. When it's done you'll have a
**Goon Studio** icon on your desktop.

## Getting started with DeepSeek (about 10 minutes of your time, then DeepSeek works for a while)

1. Install the **DeepSeek Harness desktop app** for Windows from
   [deepseek.com/en/harness](https://deepseek.com/en/harness/).
2. **Make a DeepSeek account** at [platform.deepseek.com](https://platform.deepseek.com/) - the
   **Google login** is the easiest - and **add credits** there (Billing / Top up). The desktop app
   runs on those credits, so you do not need to create or paste an API key anywhere.
3. Open DeepSeek Harness and **sign in with the same account**. In the first-run introduction,
   choose **"Full details"** (show everything) rather than "Results only", and turn **developer
   tools on**; the Studio's agent needs to run commands and read files, and the simplified view
   hides that.
4. Start a **new session** with your **Documents** folder as the workspace.
5. Paste this message and press Enter:

   > Please download the Goon Studio from **https://github.com/Francesco149/goon-studio** into this folder
   > and set it up for me by following its **AGENTS.md**. I'm not technical, so please do
   > everything for me and explain as you go.

   If you got the Studio as a zip file instead: unzip it, start the session **inside** the
   unzipped folder and say: *"Please set this up for me by following AGENTS.md."*
6. DeepSeek checks your PC, **asks you which drive to use** (it needs about 30 GB, more if you
   want the H3 video models), downloads ComfyUI and the models, and makes a test picture.

When it's done you'll have a **Goon Studio** icon on your desktop.

The target machine is a normal gaming PC: **8 GB of video memory and 16 GB of RAM** is the
baseline. The big models are streamed from system RAM, so they run, just slower; the agent will
tell you what to expect on your card (`docs/HARDWARE.md`).

## Making pictures and videos

Double-click **Goon Studio**. A page opens in your browser at http://127.0.0.1:8191:

- **Create**: pick a **template** (photoreal e-girl, anime, facial...), change the character and
  scene in plain words, pick a body type and framing, press **Make pictures**. The **Just made**
  strip shows the latest; click one to rate it, share it, or use it as a reference.
- **Video**: pick a **video recipe** (POV blowjob, side deepthroat, paizuri, cum shot, anime POV
  bob), pick a **keyframe from your pictures**, press **Make video**. **Recent videos** sits next
  to it; a clip can be used as the next keyframe to chain scenes.
- **My pictures**: your gallery. Pictures are **private** until you press **share**, which only
  makes them visible to the local agent - nothing is uploaded; private ones are invisible to the
  agent. You can select several and share, lock, or trash them.
- **Rounds**: test rounds the agent ran, with its notes.
- **Guide**: the recipes, in plain language.

If your PC is short on memory when you press Make, the page says so: it still makes the picture
or clip in a slower low-memory mode and tells you which open apps would free the most (a browser,
Steam, Discord...).

## Doing it by hand

Each template needs some model files. If one is missing, the page says so under the template:
which file, a download link, and the exact folder to save it in. Save it under exactly the name
shown, then close and reopen Goon Studio. [`docs/MODELS.md`](docs/MODELS.md) lists every
template's files. A few files are on Civitai, which needs a free account to download.

If you download a LoRA or a model yourself and want to try it, just tell your agent where it is. It
moves it into the models folder, notes where it came from, and tests it.

## Asking Claude or DeepSeek for help

Open a session **in the Studio's folder** (the one with this file) and just say what you want,
even vaguely:

- "Make her look less generic."
- "The strokes look right but the sound is wrong."
- "I want a chubby e-girl on a couch, like the examples but softer."
- "The page doesn't open." / "Pictures come out black." / "My disk is full."

For bigger questions the agent makes a small **round** of test pictures or clips. You judge them
in the **Rounds** tab, and it writes down what worked in `docs/` for next time.

## About the pictures

Everything here is **adult, fictional and local**. The models learned from a huge collection of
internet pictures, so now and then something can come out more revealing or weirder than you
asked for. It stays on your PC and is never shared with anyone; you can ignore it, rate it, or
tell the agent to steer away.

**No explicit picture is ever committed to the repo.** If an example is needed, it is censored
and a person approves it first (`docs/IMAGES.md`).

## If something is already set up

`my/settings.json` holds the paths (ComfyUI folder, gallery folder, ComfyUI address). The app is
started by `Goon Studio.cmd` or `kit\start.ps1`; the models and the gallery can live on another
drive. `docs/HARDWARE.md` explains what fits on an 8 GB card.

## License

The code is MIT (`LICENSE`); that covers the code, not a licence to publish what you generate.
ComfyUI (GPL-3.0) and the models are downloaded separately and keep their own licenses; check
each model's card for its own terms. The **Personal use only** terms above cover the pictures and
clips you make: nothing you generate is shared by this project.
