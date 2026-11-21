# Sound: the verdict and the open problem (2026-11-20)

**Status: unfinished - needs more research.** Sound work is a separate session. This note exists
so the finding is not lost and nobody ships a clip claiming the audio is fine. The owner's verdict
at the close of the mixed-reality session (2026-11-21) is unchanged: **the generated audio is
still not usable**, including on the mixed reality clips.

## What the owner heard

- The stroke sounds are **crunches**, like biting on something - not wet friction.
- The slurping sounds like **slurping noodles**, not a mouth sealed around a shaft.
- The sounds are **not synced to the action**: the pop/suction does not land on the stroke, the
  grunt is not on the beat.
- For a reference of better SFX, the **opalu videos** are the ones to study (author-only; see
  `AGENTS.local.md`). Do not commit them.

## Why it happens (working theory)

H3 generates audio jointly with the video, but its audio prior is dominated by speech, music and
room tone. Short, close-miked wet Foley is out of distribution: "wet suction" resolves to a
generic mouth noise, and the model has no notion of the visual stroke's phase. Prompt wording and
the `overall_soundscape` section change the texture a little, but they do not create a synced
Foley track.

## What to try next (in order)

1. **Treat the model audio as a scratch track.** Mute it, then build the sound bed separately:
   - a dedicated audio model (ACE-Step is on the boxes; a Foley/SFX model or a sample pack is the
     other route),
   - or a licensed Foley library: wet mouth, suction, pop, skin, breath, room tone,
   - cut the events to the visual beats in an editor (down stroke, held bottom, up stroke/pop,
     male grunt near the spurts).
2. **Prompt research, as a side experiment only.** Describe the Foley as material and timing,
   not emotion: "wet flesh sliding, a small suction pop at the top of the stroke, no chewing, no
   crunch, no slurp; one low male grunt on the second spurt". Test whether it removes the crunch;
   do not assume it will.
3. **Reference-driven**: study the opalu clips' Foley (what layers, what timing) and reproduce the
   layers with the audio tool. Again: reference only, never committed.

## Acceptance criteria (for the session that takes this on)

- No crunch on the stroke, no noodle-slurp on the seal.
- The pop lands on the top of the stroke; the suction is on the down stroke; the grunt is on the
  spurt; the room tone is continuous.
- The mix does not clip and the voice is not a word.
- A 5 s clip can be listened to without the picture and still read as the act.

## Where this is referenced

- `docs/FACIAL.md` and `docs/ANIME.md` both say the audio is a scratch track.
- `AGENTS.md` tells the agent not to claim the sound is solved.
- The owner's verdict is the source of truth here; do not "fix" it by turning the audio off
  silently - say what was done.

## Session 6 (2026-11-21): prompt wording test, still not solved by ear

The owner asked for better sound prompts while the anime recreation clips were made. Three
wordings were written for the same scene and used on H3 clips (`jobs/a10_clips.jsonl`):

- **A - material + timing + negatives:** "close-miked Foley, loud and present, clearly audible
  over a quiet bedroom room tone, no music and no speech: wet skin sliding, a soft suction hush
  as her lips slide down the shaft, one small wet click as they leave the head, her nose
  breathing, one short low male grunt on the spurt. No chewing, no crunching, no slurping, no
  gulp, no pouring water."
- **B - stroke timeline:** "one slow deep stroke: a soft wet hush as her mouth slides down, a
  small swallow at the bottom, a light suction pop as her lips leave the head. One wet spurt
  lands on her tongue with a soft tap, one low male groan... no chewing, no crunch, no noodle
  slurp."
- **C - subtractive:** "quiet bedroom room tone, her breath through her nose, the soft sound of
  skin on skin, one low male grunt at the spurt. No mouth sounds, no wet suction, no slurping, no
  chewing, no crunching, no music, no speech."

`tools/sfx_report.py` gives the objective half: loudness, peak/clipping, silence, onset density,
spectral centroid/band ratios, and the correlation between the audio envelope and the picture's
motion at each lag. The previous clips measured: `k14` -27.5 dBFS, 82 clipped samples, sync
r 0.49 at -2 frames; the owner's `img_00011` -30.9 dBFS, sync r 0.31 at 11 frames (i.e. the pop
was late); the e-girl cum-first test -43.3 dBFS, sync r 0.17. "Quiet bedroom room tone" seems to
pull the whole track down; "loud and present, clearly audible" raised the paizuri clip to
-22.4 dBFS but it clipped 416 samples, while the k14 clip stayed at -45.8 dBFS. So the level
wording moves the level, not the texture, and it is not monotonic.

The texture verdict is the owner's ear: do not mark this solved from the measurements. The
current clips ship A; B and C are written and ready for the comparison. The likely answer is
still a separate Foley bed cut to the visual beats (section above), not the model's audio.

## Session 6b: the voice-only test and the audio box

Owner's verdict on the current audio: blowjob sounds are still **crunches**, spurts are **clicks**,
the moans are not fully incoherent but far off. He suggested a separate porn-TTS/SFX generator if
H3 cannot be prompted out of it.

- **Voice-only test `k15_voice_only`** (same k9 clip and seed, soundscape replaced with "no wet
  Foley and no skin sounds; only her soft breathy moans and quick breaths, one low male groan, and
  the quiet bedroom room tone ... no crunch, no clicks"). It is the direct test of whether the bad
  wet layer can be subtracted at the prompt level. Measured: -38.1 dBFS, centroid 1496 Hz, no
  clipping; the transient count is lower than the normal mix. The owner still has to listen.
- **The audio box exists.** `lame` has `ace_step_1.5_turbo_aio.safetensors` (ACE-Step 1.5 Turbo)
  and `Qwen3-TTS-12Hz-1.7B-Base` / `-VoiceDesign` under `models/qwen-tts`, plus the ComfyUI-Qwen-TTS
  custom node. The service was started and stopped again during this session. Windows cannot reach
  `10.10.10.56:8188` directly and the SSH `-L` forward through maximus timed out, so the audio work
  has to run as a script on `lame` (submit via `127.0.0.1:8188`, pull the wav over `scp` through
  maximus). That is the next sound session: Qwen3-TTS for the voice/moans, ACE-Step for a Foley
  bed, then mux with ffmpeg against the visual beats.
- Clipping warning: "loud and present" is not free - `k11` clipped 370 samples (peak +2.6 dBFS)
  while `k16` did not. Check `tools/sfx_report.py` on every final.
