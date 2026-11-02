# YouTube MP3 Downloader

[![CI](https://github.com/WildPasta/youtube_mp3_downloader/actions/workflows/ci.yml/badge.svg)](https://github.com/WildPasta/youtube_mp3_downloader/actions/workflows/ci.yml)

## Overview
YouTube MP3 Downloader is a web application built with Flask that allows users to download audio files from YouTube videos. Simply provide the YouTube video URL, and the application extracts the audio and converts it to a genuine 192 kbps MP3 file.

## Features
- Download audio from YouTube videos as real MP3 files (converted with ffmpeg)
- Modern, responsive web interface with automatic dark mode
- Batch downloads from a `.txt` file, returned as a single `.zip` archive
- Loading indicators and inline error messages in the UI
- Files larger than 1 GB are skipped; temp folder cleanup prevents disk exhaustion
- Served by gunicorn inside a hardened Docker image (non-root user, healthcheck)

## Requirements
- Python 3.11+
- [ffmpeg](https://ffmpeg.org) - audio conversion
- [Deno](https://deno.com) or Node.js ≥ 20 - JavaScript runtime required by yt-dlp for YouTube

> *Note: the Docker image bundles all of these (easiest path).*

## Quick Install (CLI)

> *Note: It's wise to setup a venv to run any Python application*

Simply follow:
```shell
git clone https://github.com/WildPasta/youtube_mp3_downloader.git
cd youtube_mp3_downloader
python -m pip install -r server/requirements.txt
```


## Usage (CLI)

1. Start the application:
   ```shell
   python server/app.py -p 8080
   ```
2. Open your web browser and visit `http://<your_server_hostname>:8080`

3. Either provide a YouTube URL in the form or submit a text (`.txt`) file formatted as follow:

```
https://www.youtube.com/watch?v=abc
https://youtu.be/def
https://www.youtube.com/shorts/ghi
```

4. Click the download button
5. Single URL will be downloaded as a file and batch download will be downloaded as a `.zip` archive

> *Note: Default port for the application is 13000*

## Docker installation

Clone the repository:
```shell
git clone https://github.com/WildPasta/youtube_mp3_downloader.git
```

Build and run using docker compose (builds the image locally):
```shell
docker compose up -d --build
```

Or build manually:
```shell
docker build -t youtube_mp3_downloader:2.0.0 .
docker run -d -p 13000:13000 youtube_mp3_downloader:2.0.0
```

## CI/CD

Every pull request runs linting (ruff), a Docker image build and import smoke tests on Python 3.11–3.13.
Pushing a `vX.Y.Z` tag validates the Docker build and creates a GitHub Release with generated notes.
Dependabot submits weekly grouped updates for GitHub Actions, Python dependencies and Docker base images.

## Todo

- [x] ~~Use *waitress* or *gunicorn* as a WSGI~~ (gunicorn since v2.0.0)
- [ ] Choose to download either the whole clip or only the audio
- [ ] CSRF protection with Flask-WTF
- [ ] Implementation of Asynchronous download for multiple client usage

## Contribution

Feel free to contribute by adding a new feature!
See [CONTRIBUTING.md](CONTRIBUTING.md) for the git workflow, commit conventions and release process.
You can reach out at contact@pastabox.dev.

## License

This project is licensed under the MIT License.
