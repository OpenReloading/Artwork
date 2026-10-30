# Artwork

## Commands

- Agents run on the host; file edits and Git stay there. Start the container with `devcontainer up --docker-path podman --workspace-folder .`; run project commands with the prefix `devcontainer exec --docker-path podman --workspace-folder .`.
- Build every mark: `devcontainer exec --docker-path podman --workspace-folder . python3 generate.py` (writes `openreloading/`, `autolever/`, `ballistics/`, `buildguide/`).
- Rejected gap variant: `devcontainer exec --docker-path podman --workspace-folder . python3 generate.py tooth` (writes `.build/variant-tooth/`).
- `.devcontainer/Dockerfile` pins the toolchain versions. No tests: check the outputs with `git status --short` after a build. A rebuild on the same toolchain is pixel-identical (`magick compare -metric AE` gives 0), the bytes can differ.

## Conventions

- `generate.py` builds every file from constants and a system font; edit the script, never the outputs.
- Do not redesign the marks: new marks reuse the cog and add one element (user, 2026-10-10).
- Branches: `main` is the only long-lived branch. Feature branches are short-lived; pull requests target `main` and are squash-merged, history stays linear.

## Construction

The sizes and angles are constants in `generate.py`, measured from the hand-made originals.

- Gap style `ring` (chosen 2026-10-10): the ring is cut flat, whole teeth either side. `tooth` (cut through the end teeth) is the rejected alternative.
- The icon viewBox is the same square centred on the cog for every mark, so all cogs render the same size. The AutoLever lever is shortened so its knob stays inside that square.
- Wordmark font: Fira Sans (SIL OFL), outlined at build time.

## Adding a mark

Add a name to `DEST` and `WORDS`, and a `mark()` branch that returns `cog(col)` plus one element (inside the ring or leaving through the gap, like the lever). Keep the cog untouched and the icon square the same.

## Where files go on GitHub

GitHub has no per-repo logo. Org avatar: `openreloading/openreloading-icon-1024.png`. Repo social preview: that repo's `*-dark-1280x640.png`. READMEs show the wordmark with `<picture>` (light/dark). AutoLever's site copies `autolever-icon.svg` as header logo and wraps it on a white rounded square for the favicon.

## Agent skills

### Issue tracker

GitHub Issues of `OpenReloading/Artwork` via `gh`, see [docs/agents/issue-tracker.md](docs/agents/issue-tracker.md).

### Triage labels

The five defaults, see [docs/agents/triage-labels.md](docs/agents/triage-labels.md).

### Domain docs

Single context: `GLOSSARY.md` and `docs/adr/` at the root, see [docs/agents/domain.md](docs/agents/domain.md).
