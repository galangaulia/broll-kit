# Upstream

This skill is copied unchanged from [Barty-Bart/motion-graphics](https://github.com/Barty-Bart/motion-graphics)
(`skills/object-separation`), commit `83355bb58f78cdb486d6a00f6cfa22e40e538f03`, on 2026-10-09. MIT licence,
© 2026 Bart: see `LICENSE` in this folder.

One file is added here, and nothing is changed: `UPSTREAM.md`. The skill itself is a single `SKILL.md`
with no code files — it writes and runs its own Python. Keep it identical to upstream so updates stay a
plain copy:

```bash
git clone https://github.com/Barty-Bart/motion-graphics vendor/motion-graphics   # or git -C vendor/motion-graphics pull
rsync -a --delete --exclude 'LICENSE*' --exclude UPSTREAM.md vendor/motion-graphics/skills/object-separation/ .claude/skills/object-separation/
cp vendor/motion-graphics/LICENSE .claude/skills/object-separation/LICENSE   # then update the commit above
```

The models it downloads (`facebook/sam2.1-hiera-{tiny,base-plus,large}`) are Apache-2.0, so a cut-out
made with them is fine in client work.

How this repo uses it (where the masks go, how a cut-out reaches the composite, the caveats) is in the
root `CLAUDE.md` under "Cut-outs", not here.
