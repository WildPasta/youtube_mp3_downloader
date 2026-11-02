# Contributing

Thanks for your interest in contributing to `youtube_mp3_downloader`!

## Git workflow

This project follows a simplified **GitHub Flow**:

- `main` is always buildable: the Docker image is expected to build from it at any time
- All changes go through short-lived branches and pull requests
- Branch naming: `feature/<topic>`, `fix/<topic>`, `chore/<topic>`
- Rebase onto `main` when your branch drifts; keep branches short-lived

## Commit messages

Use [Conventional Commits](https://www.conventionalcommits.org/):

```
feat: add playlist download support
fix: sanitize filenames containing special characters
chore: bump yt-dlp to 2026.11.x
docs: clarify local setup in README
```

## Pull requests

- One logical change per PR
- CI must pass before merging:
  - **lint** — `ruff` with `--select E4,E7,E9,F`
  - **build** — the Docker image must build
  - **smoke** — the app must install and import on Python 3.11, 3.12 and 3.13
- Self-review your diff before requesting review

## Releases

- Releases are tagged `vX.Y.Z` on `main`
- Pushing a tag triggers the Release workflow, which:
  - builds and pushes the Docker image to `ghcr.io/wildpasta/youtube_mp3_downloader` (tag + `latest`)
  - creates a GitHub Release with auto-generated notes
- Bump the `org.opencontainers.image.version` label in the `Dockerfile` to match the tag

## Local development

With Python (3.11+ required):

```
python3 -m venv venv
source venv/bin/activate
pip install -r server/requirements.txt
python server/app.py -p 13000
```

Or with Docker:

```
docker compose up --build
```

Note: MP3 conversion requires `ffmpeg`, and YouTube extraction requires a JavaScript
runtime (`deno`, or Node >= 20). Both are bundled in the Docker image; for local runs
they must be installed on your machine.

## Dependency updates

Dependabot opens weekly grouped update PRs for GitHub Actions, Python dependencies
and Docker base images. `yt-dlp` updates in particular should be merged promptly —
stale versions break as YouTube changes.
