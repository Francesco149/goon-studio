# Sound: the verdict and the open problem (2026-11-20)

**Status: not solved. Sound work is a separate session.** This note exists so the finding is not
lost and nobody ships a clip claiming the audio is fine.

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
