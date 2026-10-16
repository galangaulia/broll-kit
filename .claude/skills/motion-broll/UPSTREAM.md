# Upstream

This skill is copied unchanged from [Barty-Bart/motion-graphics](https://github.com/Barty-Bart/motion-graphics)
(`skills/motion-broll`), commit `3d83d987d658601d8a1269eb691622bdcd427335`, on 2026-10-16 (its files changed in `cbc600c`, #3: VTT transcripts, a `black` layout case, an overdamped spring case, a `tpad` duration fix, and `os.system`/`execSync` replaced with `subprocess.run`/`execFileSync`). MIT licence, © 2026 Bart: see `LICENSE`
in this folder. Geist fonts: SIL Open Font License (`engine/fonts/OFL-Geist.txt`). Icon paths adapted
from Lucide (ISC), per the upstream README: its licence is in `LICENSE-lucide`.

Two files are added here, not changed: `package.json` (`"type": "commonjs"`, so that a
`"type": "module"` `package.json` further up the tree, such as a parent project's, can't make Node load
the engine's CommonJS `.js` files as ES modules) and `LICENSE-lucide`.

Keep the other files identical to upstream so updates stay a plain copy:

```bash
git clone https://github.com/Barty-Bart/motion-graphics vendor/motion-graphics   # or git -C vendor/motion-graphics pull
rsync -a --delete --exclude 'LICENSE*' --exclude UPSTREAM.md --exclude package.json vendor/motion-graphics/skills/motion-broll/ .claude/skills/motion-broll/
cp vendor/motion-graphics/LICENSE .claude/skills/motion-broll/LICENSE   # then update the commit above
```

How this repo uses it (folders, brand, what gets committed) is in the root `CLAUDE.md`, not here.
