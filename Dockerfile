FROM python:3.9-slim-buster

LABEL version="1.0"
LABEL maintainer="Wildpasta <chauve.richard@protonmail.com>"
LABEL repository="https://github.com/WildPasta/youtube_mp3_downloader"
LABEL description="Docker container for Youtube Downloader"

ENV DIR=/home/youtube_downloader/
WORKDIR $DIR/server

COPY server $DIR/server

RUN pip install --no-cache-dir -r requirements.txt

EXPOSE 13000

CMD ["python", "app.py"]

