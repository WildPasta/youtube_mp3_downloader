FROM denoland/deno:latest AS deno

FROM python:3.13-slim

LABEL org.opencontainers.image.version="1.0"
LABEL org.opencontainers.image.maintainer="Wildpasta <contact@pastabox.dev>"
LABEL org.opencontainers.image.repository="https://github.com/WildPasta/youtube_mp3_downloader"
LABEL org.opencontainers.image.description="Docker container for Youtube Downloader"

# ffmpeg is required for MP3 conversion, Deno for YouTube JavaScript challenges
RUN apt-get update && apt-get install -y --no-install-recommends ffmpeg \
    && rm -rf /var/lib/apt/lists/*

COPY --from=deno /deno /usr/local/bin/deno

WORKDIR /home/youtube_downloader/server

COPY server .

RUN pip install --no-cache-dir -r requirements.txt

EXPOSE 13000

CMD ["python", "app.py"]
