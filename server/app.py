from flask import Flask, render_template, request, send_file, redirect, url_for
from pytube import YouTube
from moviepy.editor import AudioFileClip
import os
import re
from urllib.parse import quote
import glob

app = Flask(__name__)

@app.route('/')
def index():
    error_message = request.args.get('error')
    return render_template('index.html', error_message=error_message)

@app.route('/download', methods=['POST'])
def download(): 
    allowed_mime_types = ['audio/mp4', 'audio/webm', 'audio/ogg', 'audio/mpeg']
    url = request.form['url']

    # Check if it is a valid YouTube URL
    if not is_valid_youtube_url(url):
        error_message = "Invalid YouTube URL"
        write_log(error_message)
        return redirect(url_for('index', error=error_message))

    # Extract audio from YouTube video
    youtube = YouTube(url)
    title = quote(youtube.title + '.mp3', safe='')
    audio = youtube.streams.filter(only_audio=True).first()

    if audio.mime_type not in allowed_mime_types:
        error_message = "Unsupported audio format"
        write_log(error_message)
        return redirect(url_for('index', error=error_message))
    
    if audio.filesize_gb > 1:
        error_message = "File is too large to be downloaded"
        write_log(error_message)
        return redirect(url_for('index', error=error_message))
    
    # Check if the temp folder exists
    if not os.path.exists('temp'):  
        os.makedirs('temp')
    temp_audio_path = os.path.join('temp', title)

    # Run cleanup if needed to prevent disk space from running out
    cleanup_temp_folder_if_needed()

    # Download audio file
    audio_file = audio.download(output_path='temp', filename=title)
    print("Audio file downloaded: ", title)

    # Write the file on disk as an MP3 file
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

def cleanup_temp_folder_if_needed():
    folder = 'temp'
    total_size = sum(os.path.getsize(file) for file in glob.glob(f"{folder}/*"))
    total_size_gb = total_size / (1024 ** 3)

    if total_size_gb > 2:
        try:
            print("Cleaning up temp folder...")
            for file in glob.glob(f"{folder}/*"):
                os.remove(file)
            print("Temp folder cleaned.")
        except Exception as e:
            print(f"Failed to delete file {file}: {e}")

    else:
        print("No cleanup needed.")

def write_log(message):
    print("An error occurred:", message)
        
if __name__ == '__main__':
    app.run(host='0.0.0.0', port=13000)
