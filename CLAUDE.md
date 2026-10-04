# B-roll studio — house rules

Motion-graphic B-roll for a talking-head video that already exists (reels,
YouTube), timed to the transcript. The `/motion-broll` skill
(`.claude/skills/motion-broll`, copied from Barty-Bart/motion-graphics, MIT)
walks the whole workflow; this file holds the choices this repo adds on top.
Read both before starting an edit.

Films made from nothing in code (Remotion, beat grid, synthesized sound) are a
different job: they live in [motion-kit](https://github.com/galangaulia/motion-kit).

## Layout

- `.claude/skills/motion-broll` the skill and its HTML engine, a plain copy of upstream. Don't edit its files in place (`UPSTREAM.md` says how to update); house-specific choices go in this file.
- `edits/<slug>` one video per folder, used as the skill's `motion/` folder. Committed: `clips/*.html`, `plan.json`, `out/TIMING.md`. Not committed: `inputs/` (footage, transcript, brand files), `work/`, `dist/`, the rest of `out/`, and the Playwright install.
- `vendor/` third-party kits, read-only, git-ignored. Check each one's licence before reusing anything (see `vendor/README.md`); a kit without a licence is reference only.
- `studio/` optional private work with the same layout (`studio/edits/<slug>`), in its own git repo and ignored here. Never `git add -f` anything under it. Edits of a real person's footage belong there, not in the kit.

## Setup

- Needs Node, Python 3 + numpy, and a full ffmpeg with `prores_ks` (transparent panels are ProRes 4444). Remotion's bundled ffmpeg lacks `overlay`, `fps` and `tmix`, so it won't do.
- Once per edit: `bash .claude/skills/motion-broll/scripts/setup.sh "$PWD/edits/<slug>"` (an absolute path: upstream's script fails on a relative one), then put the source video and its SRT in `edits/<slug>/inputs/`.

## Look

- When a brand is given, colour, type and logo come from it alone, never the skill's default palette. Copy its tokens, fonts and logo into the edit's `inputs/` and pass them in at the skill's interview. A brand kept in motion-kit has them in `brands/<name>/` there.
- One accent colour, the brand's UI face (plus a mono face for code and file names), unless the edit asks for more.
- Show the real product. Capture it instead of rebuilding it from memory; a screen that has to be rebuilt is listed in `plan.json` → `notes` as recreated, so it shows up in `TIMING.md`.
- Check the stills at 360 px wide, the size of a phone feed. When something doesn't read, cut words before shrinking type.
- Steer clear of the stock-template look. Some usual suspects: confetti or particle bursts; glitch, spin and light-leak transitions; UI that wobbles; glowing buttons and panels; a lone headline centred on a gradient.
- Nothing flashes more than three times a second (WCAG 2.3.1).

## Truth

- Never invent numbers, results, prices, quotes, customers or logos on screen. Use what the speaker says or the owner hands over; otherwise relative bars, skeleton lines or words from the transcript, listed as illustrative in `plan.json` → `notes`.
- A brand with a `brand.json` (motion-kit) brings its voice and proof rules: follow them.

## Commands

```bash
bash .claude/skills/motion-broll/scripts/setup.sh "$PWD/edits/<slug>"   # once per edit; absolute path
# video + .srt (and brand files) → edits/<slug>/inputs/, then in Claude Code: /motion-broll
```
