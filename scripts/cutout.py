"""Turn the object-separation skill's per-frame masks into a cut-out with alpha,
so a clip can sit *behind* the speaker in the composite.

    python3 scripts/cutout.py edits/<slug>/inputs/talk.mp4 \
        --masks edits/<slug>/work/masks/speaker --range 0-89 \
        --out edits/<slug>/work/speaker.mov --stills edits/<slug>/work/cutout

The skill (`.claude/skills/object-separation`) writes one hard-edged binary PNG per
frame at 960 px wide, named by absolute frame number. That is an honest mask but not
a compositing matte, so this does the three things it is missing: scales it back to
the source resolution, averages it over a few frames (`--smooth`) so the edge stops
chattering, and feathers it (`--feather`) so it stops aliasing. `--shrink` pulls the
edge in first, which kills the fringe of background colour that otherwise rims the
subject.

The output format follows `--out`: a `.mov` is ProRes 4444, the same encoder settings as
the skill's transparent panels, so `composite.py` overlays it with no extra handling; a
`.webm` is VP9 with alpha, which is what a motion-kit film's `public/clips/` takes, so a
cut-out can go into a film made from nothing in code. Everything is one ffmpeg call; only
Python's standard library and a full ffmpeg are needed.

Written for: anyone editing in this repo, agent or human. No part of it needs Claude.
"""

import argparse
import json
import pathlib
import subprocess
import sys

# Encoders with an alpha channel, by output extension. ProRes 4444 matches the skill's
# transparent panels (broll-kit); VP9 matches a motion-kit film's public/clips/.
ENCODERS = {
    '.mov': ['-c:v', 'prores_ks', '-profile:v', '4', '-pix_fmt', 'yuva444p10le', '-vendor', 'apl0'],
    '.webm': ['-c:v', 'libvpx-vp9', '-pix_fmt', 'yuva420p', '-b:v', '0', '-crf', '18', '-auto-alt-ref', '0'],
}


def probe(video):
    """Width, height and frame rate of the first video stream, as ints and a Fraction string."""
    out = subprocess.run(
        ['ffprobe', '-v', 'error', '-select_streams', 'v:0', '-show_entries',
         'stream=width,height,r_frame_rate,avg_frame_rate', '-of', 'json', str(video)],
        capture_output=True, text=True, check=True).stdout
    s = json.loads(out)['streams'][0]
    rate = s['r_frame_rate'] if s['r_frame_rate'] != '0/0' else s['avg_frame_rate']
    if s['r_frame_rate'] != s.get('avg_frame_rate') and s.get('avg_frame_rate') not in (None, '0/0'):
        print(f'note: r_frame_rate {s["r_frame_rate"]} != avg_frame_rate {s["avg_frame_rate"]}; if the video is '
              f'variable frame rate, convert it first (ffmpeg -i in.mp4 -vsync cfr -r 30 out.mp4)', file=sys.stderr)
    return int(s['width']), int(s['height']), rate


def masks_for(mask_dir, start, end):
    """The mask files covering frames start..end, checked for gaps. Returns (pattern, digits)."""
    files = sorted(p for p in mask_dir.iterdir() if p.suffix == '.png' and p.stem.isdigit())
    if not files:
        sys.exit(f'no NNNNN.png masks in {mask_dir}: run the object-separation skill first')
    digits = len(files[0].stem)
    have = {int(p.stem) for p in files}
    missing = [f for f in range(start, end + 1) if f not in have]
    if missing:
        sys.exit(f'{mask_dir} has no mask for frame(s) {missing[:8]}{"…" if len(missing) > 8 else ""}: '
                 f'it covers {min(have)}–{max(have)}, you asked for {start}–{end}')
    return str(mask_dir / f'%0{digits}d.png'), digits


def chain(width, height, start, end, smooth, shrink, feather):
    """The filter_complex: source frames start..end, the masks as their alpha."""
    frames = end - start + 1
    v = [f"[0:v]select='between(n\\,{start}\\,{end})',setpts=N/FRAME_RATE/TB,format=yuv444p10le[v]"]
    a = ['[1:v]format=gray']
    # tmix averages the window ending at the current frame, so the mask input starts
    # smooth//2 frames late to centre it, and the tail is cloned to fill the window.
    if smooth > 1:
        a.append(f'tpad=stop_mode=clone:stop_duration={smooth}')
        a.append(f'tmix=frames={smooth}')
    a.append(f'scale={width}:{height}:flags=bilinear')
    a += ['erosion'] * shrink
    if feather > 0:
        a.append(f'gblur=sigma={feather}')
    a.append('format=gray[a]')
    return ';'.join(v + [','.join(a), f'[v][a]alphamerge,trim=end_frame={frames},format=yuva444p10le[out]'])


def main():
    ap = argparse.ArgumentParser(description='Masks from the object-separation skill + the source video -> a cut-out with alpha.')
    ap.add_argument('video', type=pathlib.Path, help='the source video the masks were made from')
    ap.add_argument('--masks', required=True, type=pathlib.Path, help='folder of NNNNN.png masks (white = subject)')
    ap.add_argument('--range', required=True, help='frames to cut out, e.g. 0-89 (the range you separated)')
    ap.add_argument('--out', required=True, type=pathlib.Path,
                    help='the file to write: .mov for ProRes 4444 (broll-kit), .webm for VP9 (motion-kit clips)')
    ap.add_argument('--smooth', type=int, default=3, metavar='N',
                    help='average the mask over N frames to stop the edge chattering (1 = off, default 3)')
    ap.add_argument('--feather', type=float, default=1.2, metavar='PX',
                    help='Gaussian sigma on the mask edge, in source pixels (0 = off, default 1.2)')
    ap.add_argument('--shrink', type=int, default=1, metavar='N',
                    help='erode the mask N px before feathering, to drop the background fringe (default 1)')
    ap.add_argument('--stills', type=pathlib.Path, metavar='DIR',
                    help='also write first/middle/last frame over magenta, to check the edge before rendering')
    args = ap.parse_args()

    try:
        start, end = (int(n) for n in args.range.split('-'))
    except ValueError:
        sys.exit(f'--range must be two frame numbers, as 0-89, not {args.range!r}')
    if end < start:
        sys.exit(f'--range {args.range}: the end frame is before the start')
    if args.smooth < 1:
        sys.exit('--smooth is a frame count, 1 or more (1 = off)')
    if not args.video.is_file():
        sys.exit(f'no such video: {args.video}')
    if not args.masks.is_dir():
        sys.exit(f'no such mask folder: {args.masks}')
    encoder = ENCODERS.get(args.out.suffix.lower())
    if not encoder:
        sys.exit(f'--out {args.out.name}: the extension picks the encoder, and only '
                 f'{" or ".join(sorted(ENCODERS))} carry an alpha channel')

    width, height, rate = probe(args.video)
    pattern, _ = masks_for(args.masks, start, end)
    args.out.parent.mkdir(parents=True, exist_ok=True)

    fc = chain(width, height, start, end, args.smooth, args.shrink, args.feather)
    cmd = ['ffmpeg', '-loglevel', 'error', '-y',
           '-i', str(args.video),
           '-framerate', rate, '-start_number', str(start + args.smooth // 2), '-i', pattern,
           '-filter_complex', fc, '-map', '[out]', '-r', rate, *encoder, str(args.out)]
    subprocess.run(cmd, check=True)
    frames = end - start + 1
    print(f'wrote {args.out}  {width}×{height}  frames {start}–{end} ({frames})  '
          f'{encoder[1]}  smooth {args.smooth}  shrink {args.shrink}  feather {args.feather}')

    if args.stills:
        args.stills.mkdir(parents=True, exist_ok=True)
        picks = sorted({0, frames // 2, frames - 1})
        for i in picks:
            png = args.stills / f'{start + i:05d}.png'
            subprocess.run(['ffmpeg', '-loglevel', 'error', '-y', '-i', str(args.out),
                            '-filter_complex', f"color=magenta:s={width}x{height}[bg];"
                                               f"[0:v]select='eq(n\\,{i})'[c];[bg][c]overlay=shortest=1",
                            '-frames:v', '1', str(png)], check=True)
        print(f'stills over magenta: {", ".join(str(args.stills / f"{start + i:05d}.png") for i in picks)}')
        print('look at them at 100 %: a halo or a stair-stepped edge means more --shrink or --feather; '
              'a flickering edge across frames means more --smooth.')


if __name__ == '__main__':
    main()
