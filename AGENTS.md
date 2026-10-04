# Agent instructions

For coding agents other than Claude Code: Codex, Gemini CLI, Cursor, Copilot
and the like. Nothing in the kit needs Claude (the engine is plain Node,
Python and ffmpeg, the rules are Markdown), but the rules were written for
Claude Code first. Start here.

## Read first

1. [`CLAUDE.md`](CLAUDE.md), in full, before starting an edit. These are the house rules (layout, setup, look, truth) and they bind every agent, not only Claude.
2. `.claude/skills/motion-broll/SKILL.md`: the workflow itself. `CLAUDE.md` adds to it and wins where they differ.
3. `CLAUDE.local.md`, if it exists: notes for this machine only, git-ignored.
4. Working under `studio/`? It is a separate private repo with rules of its own: read `studio/AGENTS.md` as well.

## Where the rules assume Claude Code

- **The `/motion-broll` skill** is linked at `.agents/skills/motion-broll` for tools that load skills from there (Codex, Gemini CLI). If yours doesn't, read the file above when someone hands over a video and asks for B-roll, motion graphics or overlays, and follow its steps in order, the stop for plan approval included. `$SKILL` in it means `.claude/skills/motion-broll`.
- **AskUserQuestion** (the interview): ask the same questions in one message and wait for the answers.
- **Looking at stills**: the skill checks contact sheets of PNG stills. If your tool can't open images, hand the sheets to the user instead of skipping the check.
