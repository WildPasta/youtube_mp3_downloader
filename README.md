# YouTube Downloader

## Overview
YouTube Downloader is a web application built with Flask that allows users to download audio files from YouTube videos. Simply provide the YouTube video URL, and the application will extract the audio and provide a download link for the converted MP3 file.

## Features
- Download audio from YouTube videos as MP3 files.
- User-friendly web interface.
- Automatic file cleanup of temporary files.

## Installation
1. Clone the repository:
   ```shell
   git clone https://github.com/WildPasta/youtube_mp3_downloader.git
   ```
2. Navigate to the project directory
3. Install the required dependencies:
   ```shell
   python -m pip install -r requirements.txt
   ```

## Usage

1. Start the application on your server:
   ```shell
   python app.py
   ```
2. Open your web browser and visit `http://<your_server_hostname>:13000`.

3. Enter the YouTube video URL in the provided input field.

4. Click the "Download" button.

5. The application will extract the audio from the YouTube video and provide a download link for the converted MP3 file. Simply click the download link to save the file to your local machine.

## Todo

- [ ] CSRF protection with Flask-WTF
- [ ] Implementation of Asynchronous download for multiple client usage

## Contribution

Feel free to contribute by adding a new feature or implement function listed in the Todo section.

## License

This project is licensed under the MIT License.
