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
- `.claude/skills/object-separation` a second upstream copy, same author and licence: separates a person, product or hand from the background with SAM 2.1, on this machine. Same rule, don't edit it. What this house does with its masks is "Cut-outs" below.
- `scripts/` this repo's own tools, not upstream's. `cutout.py` turns those masks into a cut-out with alpha that the composite can stack.
- `AGENTS.md`, `GEMINI.md`, `.agents/skills/` the way in for other agents (Codex, Gemini CLI, Cursor, Copilot). When a rule here starts leaning on a Claude Code feature, say in `AGENTS.md` how to do it without one.
- `edits/<slug>` one video per folder, used as the skill's `motion/` folder. Committed: `clips/*.html`, `plan.json`, `out/TIMING.md`. Not committed: `inputs/` (footage, transcript, brand files), `work/`, `dist/`, the rest of `out/`, and the Playwright install.
- `vendor/` third-party kits, read-only, git-ignored. Check each one's licence before reusing anything (see `vendor/README.md`); a kit without a licence is reference only.
- `studio/` optional private work with the same layout (`studio/edits/<slug>`), in its own git repo and ignored here. Never `git add -f` anything under it. Edits of a real person's footage belong there, not in the kit.

## Setup

- Needs Node, Python 3 + numpy, and a full ffmpeg with `prores_ks` (transparent panels are ProRes 4444). Remotion's bundled ffmpeg lacks `overlay`, `fps` and `tmix`, so it won't do.
- Once per edit: `bash .claude/skills/motion-broll/scripts/setup.sh "$PWD/edits/<slug>"` (an absolute path: upstream's script fails on a relative one), then put the source video and its SRT in `edits/<slug>/inputs/`.
- Only for cut-outs: the object-separation skill builds its own `.object-separation` venv (torch, transformers) and downloads a SAM 2.1 model the first time. Build the venv inside the edit folder, where `.gitignore` covers it, and never at the repo root. Both are disposable; its `SKILL.md` says how to delete them.

## Workflow

Two stops, not one. The skill stops for the plan (its step 4); stop again
after the stills (step 6). Once the sheets look right to you, show them to the
user and wait for a yes before rendering (step 7): a render takes four
subframes per frame, so a wrong look costs a whole render to find.

## Look

- When a brand is given, colour, type and logo come from it alone, never the skill's default palette. Copy its tokens, fonts and logo into the edit's `inputs/` and pass them in at the skill's interview. A brand kept in motion-kit has them in `brands/<name>/` there.
- One accent colour, the brand's UI face (plus a mono face for code and file names), unless the edit asks for more.
- Show the real product. Capture it instead of rebuilding it from memory; a screen that has to be rebuilt is listed in `plan.json` → `notes` as recreated, so it shows up in `TIMING.md`.
- Check the stills at 360 px wide, the size of a phone feed. When something doesn't read, cut words before shrinking type.
- No words leave before they can be read: about three words a second, plus half a second. The speaker keeps talking, so a label that flashes past is lost; give it fewer words rather than less time.
- In a 9:16 edit, words, the product and what the cursor points at stay clear of the apps' own buttons and captions: the top 14 %, the bottom 35 % and 6 % at each side (Meta's Reels guidance), and on the right about 18 % from 45 % down, where TikTok's and Shorts' buttons sit. Check the stills against those bands.
- Steer clear of the stock-template look. Some usual suspects: confetti or particle bursts; glitch, spin and light-leak transitions; UI that wobbles; glowing buttons and panels; a lone headline centred on a gradient. Glass and refraction only when the product's own UI has them, and then capture it.
- Nothing flashes more than three times a second (WCAG 2.3.1).

## Cut-outs (a clip behind the speaker)

Every clip the skill makes sits in front of the speaker: `composite.py` overlays
them on the source in order. A cut-out buys the one thing that order can't — a
graphic that passes *behind* them, which they can turn and gesture at — and it
rescues a label that the speaker's head would otherwise cover.

- In front is the default and needs no cut-out. Behind is a deliberate choice, so it belongs in `plan.json` → `notes` for that clip ("behind the speaker"), where the plan stop can catch it. Don't decide it during the build.
- Per shot, not per edit. Separate only the span that needs it: it costs minutes a shot on Apple Silicon and about five seconds a frame on a plain CPU.
- The order is: run the object-separation skill on that span → its masks to `edits/<slug>/work/masks/<subject>/` → `scripts/cutout.py` → `work/<subject>.mov` → add that `.mov` to `plan.json` → `clips` **last** among the clips covering the span, so it lands on top.
- The skill's masks are hard-edged, binary and 960 px wide: a mask, not a matte. `cutout.py` is what makes them composite-grade (back to source resolution, averaged over frames so the edge stops chattering, feathered, eroded a px to drop the background fringe). Don't feed raw masks to the composite.
- Check `cutout.py --stills` at 100 % before rendering, as part of the stills stop. A halo or a stair-stepped edge means more `--shrink` or `--feather`; an edge that flickers between frames means more `--smooth`.
- Hair is where SAM 2 gives up. A medium shot is usually clean; a close-up may not be. If the edge won't come good in two tries, drop the idea and put the graphic beside the speaker instead. A crawling edge reads as broken, and shipping one costs more than the shot is worth.
- A cut-out of a real person's footage is private work: it belongs in `studio/`, like the footage it came from.
- `cutout.py` picks its encoder from the output extension. `.mov` is ProRes 4444, for the composite here. `.webm` is VP9 with alpha, which is what a [motion-kit](https://github.com/galangaulia/motion-kit) film's `public/clips/` takes — the same encoder settings it uses for its own clips, so a cut-out made here can go into a film made from nothing in code.

## Truth

- Never invent numbers, results, prices, quotes, customers or logos on screen. Use what the speaker says or the owner hands over; otherwise relative bars, skeleton lines or words from the transcript, listed as illustrative in `plan.json` → `notes`.
- A brand with a `brand.json` (motion-kit) brings its voice and proof rules: follow them.

## Gotchas (on top of the skill's)

- Never put `opacity` or `filter` on a `preserve-3d` element: it flattens and both faces show. Fade its wrapper.
- Inside a hidden parent, children use `visibility: inherit`; `visible` shows through.
- Words hand over through the engine's content swap (`M.vis`) or a mask, never by morphing one glyph's outline into another.

## Commands

```bash
bash .claude/skills/motion-broll/scripts/setup.sh "$PWD/edits/<slug>"   # once per edit; absolute path
# video + .srt (and brand files) → edits/<slug>/inputs/, then in Claude Code: /motion-broll

# a clip behind the speaker: /object-separation on the span, then its masks →
python3 scripts/cutout.py edits/<slug>/inputs/talk.mp4 \
  --masks edits/<slug>/work/masks/speaker --range 240-329 \
  --out edits/<slug>/work/speaker.mov --stills edits/<slug>/work/cutout
python3 scripts/cutout.py --help      # --smooth, --feather, --shrink
```
