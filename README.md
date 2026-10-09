# broll-kit

Motion-graphic B-roll for a talking-head video you already have, timed to your
words. Open [Claude Code](https://claude.com/claude-code) in this folder, drop
in a video and its transcript, and run `/motion-broll`. You get full-frame
cutaways, or transparent ProRes panels for the empty space beside you, plus a
preview cut and a before/after page. Codex, Gemini CLI, Cursor or Copilot work
too: they start from `AGENTS.md` (Gemini from `GEMINI.md`), which points to the
same rules and skills.

Want a graphic to pass *behind* you, so you can turn and gesture at it? Run
`/object-separation` on that one shot, then `scripts/cutout.py`, and the
composite stacks you back on top. See "Cut-outs" in `CLAUDE.md`.

Both skills and the engine are [Barty-Bart/motion-graphics](https://github.com/Barty-Bart/motion-graphics)
(MIT), copied unchanged. This repo adds house rules in `CLAUDE.md` (your
brand's look instead of the default palette, no invented numbers on screen, a
phone-size check, a stop to approve stills before the slow render, the 9:16
safe zone) and one folder per edit, where the plan and clips are kept in
git and the footage stays on your machine.

Making a film from nothing in code instead (launch reel, teaser, promo)? That's
[motion-kit](https://github.com/galangaulia/motion-kit).

## Setup

Node, Python 3 with numpy, and a full ffmpeg build with `prores_ks`
(Homebrew's works; Remotion's bundled one doesn't). Cut-outs add nothing to
that list up front: the object-separation skill builds its own throwaway venv
and downloads a SAM 2.1 model the first time you ask for one. It runs on the
CPU of any 8 GB machine, and much faster on Apple Silicon or an NVIDIA card.

```bash
bash .claude/skills/motion-broll/scripts/setup.sh "$PWD/edits/my-talk"   # once per edit: folders + Playwright/Chromium (absolute path)
# put the video and its .srt in edits/my-talk/inputs/ (and your brand's colours, fonts, logo), then in Claude Code:
/motion-broll
```

The skill asks a few questions (how dense, which look, what to leave alone),
shows a plan with one row per clip for you to approve, then builds and shows
you stills on the key words to approve before it renders. Everything lands in
`edits/my-talk/out/`: the clips, named by their in-point, `TIMING.md`,
`preview.mp4`, `viewer.html` and `compare.html`. The preview is for review:
place the clips in your own editor for the final cut.

## Structure

```text
CLAUDE.md                      house rules (look, truth, layout)
AGENTS.md · GEMINI.md          the way in for other agents (Codex, Gemini CLI, Cursor, Copilot)
.claude/skills/                two skills, both upstream copies (see each UPSTREAM.md), linked from .agents/skills/
  motion-broll/                B-roll timed to the transcript: the skill and its HTML engine
  object-separation/           separate a subject from the background, with SAM 2.1, on your machine
scripts/cutout.py              this repo's own: masks -> a cut-out with alpha (.mov here, .webm for motion-kit)
edits/<slug>/                  one video per folder, made by setup.sh
  inputs/                      footage, transcript, brand files    (not committed)
  clips/*.html · plan.json     the clips and the plan              (committed)
  out/                         renders, preview, pages             (only TIMING.md committed)
vendor/                        upstream clone, for updates (git-ignored, see vendor/README.md)
```

## Private work: `studio/`

Edits of your own or a client's footage that you don't want in a public fork
can live in `studio/`, a separate git repo nested here and ignored by this one,
with the same layout. Give it the same `edits/` rules from `.gitignore`.

```bash
mkdir -p studio/edits && git -C studio init
bash .claude/skills/motion-broll/scripts/setup.sh "$PWD/studio/edits/my-talk"
```

## Licences

- This repo: [MIT](LICENSE).
- `.claude/skills/motion-broll` and `.claude/skills/object-separation`: MIT, © 2026 Bart ([Barty-Bart/motion-graphics](https://github.com/Barty-Bart/motion-graphics)), copied unchanged; Geist fonts SIL Open Font License 1.1; Lucide icon paths ISC. Licences and the upstream commit are in each folder.
- The SAM 2.1 models object-separation downloads (`facebook/sam2.1-hiera-*`): Apache-2.0, so a cut-out made with them is fine in client work.
- `vendor/` kits keep their own licences; see `vendor/README.md`.
