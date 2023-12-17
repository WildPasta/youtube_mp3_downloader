# YouTube Downloader

## Overview
YouTube Downloader is a web application built with Flask that allows users to download audio files from YouTube videos. Simply provide the YouTube video URL, and the application will extract the audio and provide a download link for the converted MP3 file.

## Features
- Download audio from YouTube videos as MP3 files
- User-friendly web interface
- Download batch from file
- File cleanup of download folder

## Quick Install (CLI)

Simply follow:
```shell
git clone https://github.com/WildPasta/youtube_mp3_downloader.git
cd youtube_mp3_downloader
python -m pip install -r requirements.txt
```

> *Note: It's wise to setup a venv to run any Python application*

## Usage (CLI)

1. Start the application:
   ```shell
   python app.py -p 8080
   ```
2. Open your web browser and visit `http://<your_server_hostname>:8080`

3. Either provide a YouTube URL in the form or submit a text (`.txt`) file formatted as follow:

```
https://www.youtube.com/watch?v=abc
https://www.youtube.com/watch?v=def
https://www.youtube.com/watch?v=ghi
```

4. Click the download button
5. Single URL will be downloaded as a file and batch download will be downloaded as a `.zip` archive

> *Note: Default port for the application is 13000*

## Docker installation

Clone the repository:
```shell
git clone https://github.com/WildPasta/youtube_mp3_downloader.git
```

Build the docker image:
```shell
docker build -t wildpasta/youtube_downloader:1.2.0 . --rm
```

Run the docker container using the docker-compose.yml file:
```shell
docker-compose up -d
```
## Todo

- [ ] Use *waitress* or *gunicorn* as a WSGI
- [ ] Choose to download either the whole clip or only the audio
- [ ] CSRF protection with Flask-WTF
- [ ] Implementation of Asynchronous download for multiple client usage

## Contribution

Feel free to contribute by adding a new feature!
You can reach out at chauve.richard@protonmail.com.

## License

This project is licensed under the MIT License.
