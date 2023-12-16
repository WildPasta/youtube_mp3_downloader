##########
# Author: wildpasta
# Description: A simple Flask app that downloads audio from YouTube videos
# Usage: python app.py -p <port>
# Example: python app.py -p 13000
##########

# Python standard libraries
import argparse
import os
import re
import glob
from urllib.parse import quote

# Third-party libraries
from flask import Flask, render_template, request, send_file, redirect, url_for
from pytube import YouTube
from typing import Tuple
from werkzeug.utils import secure_filename


app = Flask(__name__)

@app.route('/')
def index():
    error_message = request.args.get('error')
    return render_template('index.html', error_message=error_message)

@app.route('/download', methods=['POST'])
def download(): 
    ALLOWED_MIME_TYPES = ['audio/mp4', 'audio/webm', 'audio/ogg', 'audio/mpeg']
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

    if audio.mime_type not in ALLOWED_MIME_TYPES:
        error_message = "Unsupported audio format"
        write_log(error_message)
        return redirect(url_for('index', error=error_message))
    
    if audio.filesize_gb > 1:
        error_message = "File is too large to be downloaded"
        write_log(error_message)
        return redirect(url_for('index', error=error_message))
    
    # Create temp folder if it doesn't exist 
    os.makedirs('temp', exist_ok=True)

    # Run cleanup if needed to prevent disk space from running out
    cleanup_temp_folder_if_needed()

    # Download audio file
    audio_file = audio.download(output_path='temp', filename=title)
    print("Audio file downloaded: ", title)

    # Write the file on disk as an MP3 file
    base, ext = os.path.splitext(audio_file)
    mp3_file = base + '.mp3'
    os.rename(audio_file, mp3_file)

    # Return the MP3 file as a download
    response = send_file(mp3_file, as_attachment=True)
    response.headers["Content-Disposition"] = "attachment; filename={}".format(title)
    return response

@app.route('/batch_download', methods=['POST'])
def batch_download():
    # Check if the request contains a file
    if 'file' not in request.files:
        error_message = "No file part"
        write_log(error_message)
        return redirect(url_for('index', error=error_message))

    file = request.files['file']

    # Check if the file is empty
    if file.filename == '':
        error_message = "No selected file"
        write_log(error_message)
        return redirect(url_for('index', error=error_message))

    # Check if the file has an allowed extension
    if not allowed_file(file.filename):
        error_message = "Invalid file type"
        write_log(error_message)
        return redirect(url_for('index', error=error_message))

    # Process the URLs in the file without saving it to the server
    success_count, failure_count = process_urls_in_memory(file)

    return f"Batch download complete. {success_count} succeeded, {failure_count} failed."

def process_urls_in_memory(file) -> Tuple[int, int]:
    """
    Process URLs in a file (passed as a Flask FileStorage object) and download audio for each URL.
    """
    success_count = 0
    failure_count = 0

    # Read the file content from memory
    file_content = file.stream.read().decode('utf-8').splitlines()

    for line in file_content:
        url = line.strip()
        if is_valid_youtube_url(url):
            try:
                download_audio(url)
                success_count += 1
            except Exception as e:
                print(f"Failed to download audio from {url}: {e}")
                failure_count += 1
        else:
            print(f"Invalid YouTube URL: {url}")
            failure_count += 1

    return success_count, failure_count

def allowed_file(filename):
    ALLOWED_EXTENSIONS = ['txt']
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

def is_valid_youtube_url(url: str) -> bool:
    """
    purpose:
        Check if the URL is a valid YouTube URL
    input:
        url: str
    output:
        bool
    """

    pattern = r'^(https?\:\/\/)?(www\.youtube\.com|youtu\.?be)\/.+$'
    return re.match(pattern, url)

def cleanup_temp_folder_if_needed() -> None:
    """
    purpose: 
        Delete files in temp folder if the total size is greater than 1 GB
    input: 
        None
    output: 
        None
    """

    folder = 'temp'
    total_size = sum(os.path.getsize(file) for file in glob.glob(f"{folder}/*"))
    total_size_gb = total_size / (1024 ** 3)

    if total_size_gb > 1:
        try:
            print("Cleaning up temp folder...")
            for file in glob.glob(f"{folder}/*"):
                os.remove(file)
            print("Temp folder cleaned.")
        except Exception as e:
            print(f"Failed to delete file {file}: {e}")
    else:
        print("No cleanup needed.")

def write_log(message: str) -> None:
    """
    purpose:
        Write error message to log file
    input:
        message: str
    output:
        None
    """
    
    print("An error occurred:", message)
        
if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Youtube Download')
    parser.add_argument('-p', '--port', type=int, default=13000, help='Specify the port number')
    args = parser.parse_args()
    port = args.port
    app.run(host='0.0.0.0', port=port)

