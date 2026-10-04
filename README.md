# broll-kit

Motion-graphic B-roll for a talking-head video you already have, timed to your
words. Open [Claude Code](https://claude.com/claude-code) in this folder, drop
in a video and its transcript, and run `/motion-broll`. You get full-frame
cutaways, or transparent ProRes panels for the empty space beside you, plus a
preview cut and a before/after page.

The skill and its engine are [Barty-Bart/motion-graphics](https://github.com/Barty-Bart/motion-graphics)
(MIT), copied unchanged. This repo adds house rules in `CLAUDE.md` (your
brand's look instead of the default palette, no invented numbers on screen, a
phone-size check) and one folder per edit, where the plan and clips are kept in
git and the footage stays on your machine.

Making a film from nothing in code instead (launch reel, teaser, promo)? That's
[motion-kit](https://github.com/galangaulia/motion-kit).

## Setup

Node, Python 3 with numpy, and a full ffmpeg build with `prores_ks`
(Homebrew's works; Remotion's bundled one doesn't).

```bash
bash .claude/skills/motion-broll/scripts/setup.sh "$PWD/edits/my-talk"   # once per edit: folders + Playwright/Chromium (absolute path)
# put the video and its .srt in edits/my-talk/inputs/ (and your brand's colours, fonts, logo), then in Claude Code:
/motion-broll
```

The skill asks a few questions (how dense, which look, what to leave alone),
shows a plan with one row per clip for you to approve, then builds, checks
stills on the key words and renders. Everything lands in `edits/my-talk/out/`:
the clips, named by their in-point, `TIMING.md`, `preview.mp4`, `viewer.html`
and `compare.html`. The preview is for review: place the clips in your own
editor for the final cut.

## Structure

```text
CLAUDE.md                      house rules (look, truth, layout)
.claude/skills/motion-broll/   the skill and its engine (upstream copy, see UPSTREAM.md)
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
- `.claude/skills/motion-broll`: MIT, © 2026 Bart ([Barty-Bart/motion-graphics](https://github.com/Barty-Bart/motion-graphics)), copied unchanged; Geist fonts SIL Open Font License 1.1; Lucide icon paths ISC. Licences and the upstream commit are in that folder.
- `vendor/` kits keep their own licences; see `vendor/README.md`.
