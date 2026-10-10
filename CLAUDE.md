# Artwork

Logos of the OpenReloading org and its projects. `generate.py` builds every file from constants and a system font; edit the script, never the outputs. Build needs python3 + fontTools, Fira Sans (via fontconfig), rsvg-convert, ImageMagick 7. Do not redesign the marks: new marks reuse the cog and add one element (user, 2026-10-10).

## Construction (`generate.py`)

- Coordinates: the hand-made organisation mark's space, cog centre `CX, CY = 149.02, 625.97`. Icon viewBox is a 212.3 square centred on the cog for every mark, so all cogs render the same size.
- Cog: one closed outline. Ring 55.4–70.2, tooth tips 84.5. 9 tooth positions on a 40° pitch, the one at 37.5° (1 o'clock) left out; that is the gap. Tooth half-width 11.5° at the ring, 8° at the tip. Corners: the outline is inset by `RHO` 2.6 and stroked 5.2 with round joins.
- Gap style `ring` (chosen 2026-10-10): the ring is cut flat at 16.5° and 58.5°, whole teeth either side. `python3 generate.py tooth` builds the rejected alternative (cut through the end teeth at 6.5° / 68.5°) into `.build/`.
- OpenReloading: cog + `CASE_HEAD` (disc, primer ring, primer; the original hand-made path, scaled 0.95 for a hairline to the ring).
- AutoLever: cog + lever through the gap at 37.5°: hub r 22.7 with r 5 pivot hole, bar 21.4 wide from r 18 to r 104, knob r 22.6. Sizes measured from the hand-made lever, length shortened so the knob stays inside the icon square.
- Ballistics: cog + pressure-curve chart inside: baseline 30 below centre, curve and baseline reach 4 units into the ring on both sides, peak 38 above centre, 14 left of centre.
- Wordmarks: lettering outlined at build time from Fira Sans (SIL OFL) with fontTools, first word bold, second regular, manual kerning for Au/Le/ev/Re; project marks (AutoLever, Ballistics) get "OpenReloading" small above their name. Layout: the icon square scaled so the cog is 100 tall, text 43 (20 for the small line), 4 units gap after the square. Transparent, `color` set per variant.
- PNGs: icon 880 px white mark on a 1024 black square (avatars); `-light-1280x640.png` (black on white) and `-dark-1280x640.png` (white on black) wordmarks, 1120 px wide content. README shows both; the dark one is the GitHub social preview. Date chunks are left out so a rebuild is byte-identical.

## Adding a mark

Add a name to `DEST` and `WORDS`, and a `mark()` branch that returns `cog(col)` plus one element (inside the ring or leaving through the gap, like the lever). Keep the cog untouched and the icon square the same.

## Where files go on GitHub

GitHub has no per-repo logo. Org avatar: `openreloading/openreloading-icon-1024.png`. Repo social preview: that repo's `*-dark-1280x640.png`. READMEs show the wordmark with `<picture>` (light/dark). AutoLever's site copies `autolever-icon.svg` as header logo and wraps it on a white rounded square for the favicon.
