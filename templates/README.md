# Templates (manual runs)

The app's built-in templates live in `kit/presets.json`. This folder is for extra prompt
snippets you want to keep next to the workflows without wiring them into the page: a character
block, a scene, a negative for a specific model. Copy the block into the page's Character/Scene/
Prompt fields, or reference it from a job file for `tools/lab.py`.

Keep them as plain text or JSON; nothing here is loaded automatically. The user's own templates
go in `my/presets.json` (git-ignored) and are merged on top of the built-ins.
