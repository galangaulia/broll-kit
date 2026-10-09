# Agent instructions

For coding agents other than Claude Code: Codex, Gemini CLI, Cursor, Copilot
and the like. Nothing in the kit needs Claude (the engine is plain Node,
Python and ffmpeg, the rules are Markdown), but the rules were written for
Claude Code first. Start here.

## Read first

1. [`CLAUDE.md`](CLAUDE.md), in full, before starting an edit. These are the house rules (layout, setup, look, truth) and they bind every agent, not only Claude.
2. `.claude/skills/motion-broll/SKILL.md`: the workflow itself. `CLAUDE.md` adds to it and wins where they differ.
3. Making a clip pass behind the speaker? `.claude/skills/object-separation/SKILL.md` too, plus "Cut-outs" in `CLAUDE.md`, which wins where they differ.
4. `CLAUDE.local.md`, if it exists: notes for this machine only, git-ignored.
5. Working under `studio/`? It is a separate private repo with rules of its own: read `studio/AGENTS.md` as well.

## Where the rules assume Claude Code

- **The `/motion-broll` skill** is linked at `.agents/skills/motion-broll` for tools that load skills from there (Codex, Gemini CLI). If yours doesn't, read the file above when someone hands over a video and asks for B-roll, motion graphics or overlays, and follow its steps in order, the stops for plan and stills approval included (`CLAUDE.md` adds the second). `$SKILL` in it means `.claude/skills/motion-broll`.
- **AskUserQuestion** (the interview): ask the same questions in one message and wait for the answers.
- **Looking at stills**: the skill checks contact sheets of PNG stills. If your tool can't open images, hand the sheets to the user instead of skipping the check.
- **The `/object-separation` skill** is linked at `.agents/skills/object-separation` the same way, and needed only for a cut-out. It is one Markdown file with no code: it has you write and run its Python yourself, in a venv it builds, so any agent with a shell can follow it. Two steps lean on Claude Code, and both have a plain fallback:
  - *Picking the click points* (its step 3) means looking at one frame with a coordinate grid drawn on it. If your tool can't open images, write the grid frame to `work/preview.jpg` as the skill does, show it to the user, and ask them for the x,y of the subject and of anything to leave out. Don't guess coordinates from the transcript or the file name.
  - *Checking the result* (its step 5, and `cutout.py --stills`) means looking at frames. Same fallback: hand them to the user. Never skip it — a bad matte is only visible in the picture, and it survives all the way into the render.
- **Running Python**: `scripts/cutout.py` is standard-library-only and needs a full ffmpeg on `PATH`, nothing else. The skill's own Python needs its venv, so call it as `.object-separation/bin/python` (Windows: `.object-separation\Scripts\python`), not the system `python3`.
