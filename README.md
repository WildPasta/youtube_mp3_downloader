# YouTube Downloader

## Overview
YouTube Downloader is a web application built with Flask that allows users to download audio files from YouTube videos. Simply provide the YouTube video URL, and the application will extract the audio and provide a download link for the converted MP3 file.

## Features
- Download audio from YouTube videos as MP3 files.
- User-friendly web interface.
- Automatic file cleanup of temporary files.

## Installation (CLI)

1. Clone the repository:
   ```shell
   git clone https://github.com/WildPasta/youtube_mp3_downloader.git
   ```
2. Navigate to the project directory
3. Install the required dependencies:
   ```shell
   python -m pip install -r requirements.txt
   ```

## Usage (CLI)

1. Start the application on your server:
   ```shell
   python app.py -p 8080
   ```
2. Open your web browser and visit `http://<your_server_hostname>:8080`.

3. Enter the YouTube video URL in the provided input field.

4. Click the "Download" button.

5. The application will extract the audio from the YouTube video and provide a download link for the converted MP3 file. Simply click the download link to save the file to your local machine.

*Note: Default port for the application is 14000. If you don't specify `-p` or `--port` flag then the application will run on port 14000.*
## Docker installation

Clone the repository:
```shell
git clone https://github.com/WildPasta/youtube_mp3_downloader.git
```

Build the docker image:
```shell
docker build -t wildpasta/youtube_downloader:1.1.0 .
```

Run the docker container using the docker-compose.yml file:
```shell
docker-compose up -d
```
## Todo

- [ ] CSRF protection with Flask-WTF
- [ ] Implementation of Asynchronous download for multiple client usage

## Contribution

Feel free to contribute by adding a new feature or implement function listed in the Todo section.

## License

This project is licensed under the MIT License.
