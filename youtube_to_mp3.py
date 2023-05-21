from flask import Flask, render_template, request, send_file, redirect, url_for
from pytube import YouTube
from moviepy.editor import AudioFileClip
import os
import re
from urllib.parse import quote

app = Flask(__name__)

@app.route('/')
def index():
    error_message = request.args.get('error')
    return render_template('index.html', error_message=error_message)

@app.route('/download', methods=['POST'])
def download():
    clear_temp_folder()
    allowed_mime_types = ['audio/mp4', 'audio/webm', 'audio/ogg', 'audio/mpeg']
    url = request.form['url']

    # Check if it is a valid YouTube URL
    if not is_valid_youtube_url(url):
        error_message = "Invalid YouTube URL"
        return redirect(url_for('index', error=error_message))

    # Extract audio from YouTube video
    youtube = YouTube(url)
    title = quote(youtube.title + '.mp3', safe='')
    audio = youtube.streams.filter(only_audio=True).first()

    if audio.mime_type not in allowed_mime_types:
        error_message = "Unsupported audio format"
        return redirect(url_for('index', error=error_message))
    
    # Download audio file
    audio_file = audio.download(output_path='temp', filename=title)

    # Path to temporary audio file
    temp_audio_path = os.path.join('temp', title)

    # Convert to MP3 format
    mp3_path = os.path.join('temp', title)
    audio_clip = AudioFileClip(temp_audio_path)
    audio_clip.write_audiofile(mp3_path)

    # Return the MP3 file as a download
    response = send_file(mp3_path, as_attachment=True)
    response.headers["Content-Disposition"] = "attachment; filename={}".format(title)
    return response

def is_valid_youtube_url(url):
    pattern = r'^(https?\:\/\/)?(www\.youtube\.com|youtu\.?be)\/.+$'
    return re.match(pattern, url)

def clear_temp_folder():
    folder = 'temp'
    for filename in os.listdir(folder):
        file_path = os.path.join(folder, filename)
        try:
            if os.path.isfile(file_path):
                os.unlink(file_path)
        except Exception as e:
            print(f"Failed to delete file {file_path}: {e}")

if __name__ == '__main__':
    app.run()
