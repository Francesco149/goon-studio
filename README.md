# Goon Studio

Make explicit pictures and clips on your own PC: your own characters, any body type, any scene.
Everything runs on your computer, nothing is uploaded anywhere.

You don't need to know anything technical. **DeepSeek sets it up, keeps it working and helps you
get the pictures and clips you want.**

This is the NSFW companion of Love Live Studio. The two are separate apps with separate
galleries: Love Live Studio stays SFW, this one stays here. They never read each other's private
pictures.

## Getting started (about 10 minutes of your time, then DeepSeek works for a while)

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
baseline. The big models are streamed from system RAM, so they run, just slower; DeepSeek will
tell you what to expect on your card (`docs/HARDWARE.md`).

## Making pictures and videos

Double-click **Goon Studio**. A page opens in your browser at http://127.0.0.1:8191:

- **Create**: pick a **template** (photoreal e-girl, anime, facial...), change the character and
  scene in plain words, pick a body type and framing, press **Make pictures**. The **Just made**
  strip shows the latest; click one to rate it, share it, or use it as a reference.
- **Video**: pick a **video recipe** (POV blowjob, side deepthroat, paizuri, cum shot, anime POV
  bob), pick a **keyframe from your pictures**, press **Make video**. **Recent videos** sits next
  to it; a clip can be used as the next keyframe to chain scenes.
- **My pictures**: your gallery. Pictures are **private** until you press **share**; private ones
  are invisible to the agent. You can select several and share, lock, or trash them.
- **Rounds**: test rounds the agent ran, with its notes.
- **Guide**: the recipes, in plain language.

## Asking DeepSeek for help

Open a session **in the Studio's folder** (the one with this file) and just say what you want,
even vaguely:

- "Make her look less generic."
- "The strokes look right but the sound is wrong."
- "I want a chubby e-girl on a couch, like the examples but softer."
- "The page doesn't open." / "Pictures come out black." / "My disk is full."

For bigger questions DeepSeek makes a small **round** of test pictures or clips. You judge them
in the **Rounds** tab, and it writes down what worked in `docs/` for next time.

## About the pictures

Everything here is **adult, fictional and local**. The models learned from a huge collection of
internet pictures, so now and then something can come out more revealing or weirder than you
asked for. It stays on your PC; you can ignore it, rate it, or tell DeepSeek to steer away.

**No explicit picture is ever committed to the repo.** If an example is needed, it is censored
and a person approves it first (`docs/IMAGES.md`).

## If something is already set up

`my/settings.json` holds the paths (ComfyUI folder, gallery folder, ComfyUI address). The app is
started by `Goon Studio.cmd` or `kit\start.ps1`; the models and the gallery can live on another
drive. `docs/HARDWARE.md` explains what fits on an 8 GB card.
