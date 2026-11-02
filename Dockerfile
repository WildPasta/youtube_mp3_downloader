FROM denoland/deno:bin-2.9.8 AS deno

FROM ghcr.io/astral-sh/uv:0.13.6 AS uv

FROM python:3.13-slim

ARG VERSION=2.1.0
LABEL org.opencontainers.image.version="${VERSION}"
LABEL org.opencontainers.image.maintainer="Wildpasta <contact@pastabox.dev>"
LABEL org.opencontainers.image.repository="https://github.com/WildPasta/youtube_mp3_downloader"
LABEL org.opencontainers.image.description="Docker container for Youtube Downloader"

ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1 \
    UV_COMPILE_BYTECODE=1 \
    UV_LINK_MODE=copy

# ffmpeg is required for MP3 conversion, Deno for YouTube JavaScript challenges
RUN apt-get update && apt-get install -y --no-install-recommends ffmpeg \
    && rm -rf /var/lib/apt/lists/*

COPY --from=deno /deno /usr/local/bin/deno
COPY --from=uv /uv /uvx /usr/local/bin/

RUN useradd --create-home --uid 1000 --shell /usr/sbin/nologin appuser \
    && mkdir -p /home/youtube_downloader/server \
    && chown -R appuser:appuser /home/youtube_downloader

WORKDIR /home/youtube_downloader/server

COPY --chown=appuser:appuser pyproject.toml uv.lock ./
RUN uv sync --frozen --no-dev && chown -R appuser:appuser .venv

COPY --chown=appuser:appuser server/ .

USER appuser

ENV PATH="/home/youtube_downloader/server/.venv/bin:${PATH}"

EXPOSE 13000

HEALTHCHECK --interval=30s --timeout=5s --start-period=15s --retries=3 \
    CMD python -c "import urllib.request; urllib.request.urlopen('http://127.0.0.1:13000/', timeout=4)" || exit 1

CMD ["gunicorn", "--bind", "0.0.0.0:13000", "--workers", "2", "--threads", "4", "--timeout", "600", "app:app"]
