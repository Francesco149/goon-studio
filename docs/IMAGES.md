# Images in this repo: what may be committed

The terms of use are in **`README.md`** ("Personal use only"); this file only covers what may be
committed. The generated material never goes into the repo.

**No NSFW image is ever committed.** Not in `docs/`, not in `examples/`, not in a PR, not in a
test fixture.

If an example picture is genuinely needed in the repo (a UI screenshot, a README illustration, a
visual regression fixture), all of this must be true:

1. Every explicit part is hidden: the cock replaced or covered (the standard joke is a baguette,
   but any opaque, non-sexual prop works), genitals, anus, nipples and any sex act fully obscured.
2. The result is **vetted by a human** before `git add`. An agent must never commit a censored
   example on its own judgement; it stages it, says what it is, and waits for the human's yes.
3. It is small and named plainly (`docs/img/ui.png`), with no prompt in the metadata (strip EXIF /
   PNG text chunks).
4. It does not come from a private session or a private gallery item.

The same rule applies to video: no NSFW video, and no censored clip without human vetting.

## References

References are kept, organised and **never committed**:

- `gallery/refs/` - the working set (git-ignored with `gallery/`). Keep one subfolder per source
  and a short `INDEX.md` there describing what each clip is for; that index is local too.
- The author's own reference clips live outside the repo (see `AGENTS.local.md`, which is
  git-ignored). They are not copied in.
- If a reference must be shared with another local agent, describe it in text; do not attach the
  file, and never send it to a remote service.

## Why

The repo is public-shaped: it can be cloned, pushed or shown without leaking the user's material.
The gallery is the private part; the repo is the recipe book. The terms for the generated
material itself are in `README.md` ("Personal use only"): it stays local and is never shared.
