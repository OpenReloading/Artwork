<p align="center"><picture><source media="(prefers-color-scheme: dark)" srcset="openreloading/openreloading-dark.svg"><img src="openreloading/openreloading-light.svg" width="360" alt="OpenReloading"></picture></p>

# Artwork

Logos and wordmarks of OpenReloading and its projects. Monochrome only: black on light backgrounds, white on dark ones.

| Mark | Icon | Wordmark |
|---|---|---|
| OpenReloading (the organisation) | <img src="openreloading/openreloading-icon.svg" width="64"> | <img src="openreloading/openreloading-light.svg" width="220"> |
| AutoLever (press lever drive) | <img src="autolever/autolever-icon.svg" width="64"> | <img src="autolever/autolever-light.svg" width="220"> |
| Ballistics (calculator, database, library) | <img src="ballistics/ballistics-icon.svg" width="64"> | <img src="ballistics/ballistics-light.svg" width="220"> |

All three share the same open cog. The organisation mark holds a cartridge case head, AutoLever's lever leaves through the gap, Ballistics carries a pressure curve.

## Files

Each mark has the same set:

| File | Use |
|---|---|
| `<name>-icon.svg` | The mark alone. Transparent, draws in `currentColor`; use it in pages, headers and favicons. |
| `<name>-light.svg`, `<name>-dark.svg` | Mark with wordmark, transparent, for light and dark backgrounds. In a README use both with `<picture>`. |
| `<name>-icon-1024.png` | White mark on black, 1024 × 1024, for avatars (GitHub org picture). |
| `<name>-social-1280x640.png` | White wordmark on black, 1280 × 640, for GitHub social previews. |

GitHub has no per-repository logo. The org avatar is `openreloading/openreloading-icon-1024.png`; each repository gets its social preview from its own folder and shows its wordmark at the top of its README.

## Rules

- One colour. Do not recolour, add gradients, outlines or shadows.
- Do not close the gap in the cog, rotate the mark or separate the lever or curve from the cog.
- Keep clear space around the mark of at least one tooth height.
- Scale as a whole. Below 24 px use the icon, not the wordmark.

## Regenerating

`original/` is the hand-made set the marks are derived from. `generate.py` measures nothing at run time: the cog is drawn from the constants at the top of the script (ring radii, tooth pitch, gap angles), the case head and the lettering are copied from `original/`.

```sh
python3 generate.py          # needs rsvg-convert and ImageMagick 7 (magick)
python3 generate.py tooth    # variant with the gap cut through the end teeth, written to .build/
```

## Licence

MIT, see `LICENSE`. The names OpenReloading, AutoLever and Ballistics identify these projects; use the marks to refer to them, not to suggest endorsement of something else.
