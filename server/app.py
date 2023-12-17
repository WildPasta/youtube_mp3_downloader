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
import uuid
import zipfile
from urllib.parse import quote, unquote

# Third-party libraries
from flask import Flask, render_template, request, send_file, redirect, url_for
from pytube import YouTube

app = Flask(__name__)
LOCAL_DOWNLOAD_FOLDER = 'temp'
ALLOWED_EXTENSIONS = {'txt'}
ALLOWED_MIME_TYPES = ['audio/mp4', 'audio/webm', 'audio/ogg', 'audio/mpeg']

@app.route('/', methods=['GET'])
def index() -> None:
    """ 
    purpose: 
        render the index page
    input:  
        None
    output:
        None
    """

    try:
        error_message = request.args.get('error')
        return render_template('index.html', error_message=error_message)
    except Exception:
        return redirect(url_for('index', error="An internal error occurred..."))

@app.route('/download', methods=['POST'])
def download() -> None:
    """ 
    purpose:
        download audio from YouTube video
    input:
        None
    output:
        None
    """

    try:
        os.makedirs(LOCAL_DOWNLOAD_FOLDER, exist_ok=True)
        url = request.form['url']

        mp3_file, title = download_audio(url)
        print(f'Audio file downloaded: {title}')

        # Send the file as a download
        response = send_file(mp3_file, as_attachment=True)
        response.headers["Content-Disposition"] = "attachment; filename={}".format(title)
        return response

    except Exception:
        return redirect(url_for('index', error="An internal error occurred..."))

@app.route('/batch_download', methods=['POST'])
def batch_download():
    """
    purpose:
        download audio from YouTube videos in batch
    input:
        None
    output: 
        None
    """ 

    try:
        os.makedirs(LOCAL_DOWNLOAD_FOLDER, exist_ok=True)
        urls = []

        # Check if a file is provided
        if 'file' in request.files:
            file = request.files['file']
            
            # Ensure the file has an allowed extension
            if file and allowed_file(file.filename):
                # Read URLs from the file
                urls_from_file = [line.decode('utf-8').strip() for line in file.readlines()]
                urls.extend(urls_from_file)

        # Ensure at least one URL is provided
        if not urls:
            error_message = "No URLs provided for download."
            return redirect(url_for('index', error=error_message))

        # Run cleanup if needed to prevent disk space from running out
        cleanup_temp_folder_if_needed()

        zip_filename = str(uuid.uuid4())[:8] + '_music_archive.zip'
        zip_filepath = os.path.join(LOCAL_DOWNLOAD_FOLDER, zip_filename)

        with zipfile.ZipFile(zip_filepath, 'w') as zip_file:
            for url in urls:
                download_and_add_to_zip(zip_file, url)

        # Return the zip file as a download
        response = send_file(zip_filepath, as_attachment=True)
        response.headers["Content-Disposition"] = "attachment; filename={}".format(zip_filename)
        return response

    except Exception:
        return redirect(url_for('index', error="An internal error occurred..."))

def download_and_add_to_zip(zip_file: str, url: str) -> None:
    """
    purpose: 
        download audio from YouTube video and add to zip file
    input:
        zip_file: zip file object
        url: YouTube URL
    output:
        None
    """

    try:
        mp3_file, title = download_audio(url)
        zip_file.write(mp3_file, os.path.basename(unquote(mp3_file)))
        print("Audio file downloaded and added to zip:", title)
    except Exception as e:
        print(f"Error downloading {url}: {e}")

def allowed_file(filename: str) -> bool:
    """
    purpose:
        check if the file has an allowed extension
    input:  
        filename: name of the file
    output: 
        True if the file has an allowed extension, False otherwise
    """

    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

def download_audio(url: str) -> tuple:
    """
    purpose: 
        download audio from YouTube video
    input: 
        url: YouTube URL
    output: 
        mp3_file: path to the downloaded MP3 file
        title: title of the YouTube video
    """

    if not is_valid_youtube_url(url):
        print(f"Invalid YouTube URL: {url}")
        return
    
    # Extract audio from YouTube video
    youtube = YouTube(url)
    title = quote(youtube.title + '.mp3', safe='')
    audio = youtube.streams.filter(only_audio=True).first()

    if audio.mime_type not in ALLOWED_MIME_TYPES:
        print(f"Unsupported audio format: {audio.mime_type} for {url}")
        return
    
    elif audio.filesize_gb > 1:
        print(f"File is too large to be downloaded: {title}")
        return

    # Run cleanup if needed to prevent disk space from running out
    cleanup_temp_folder_if_needed()

    # Download audio file
    audio_file = audio.download(output_path=LOCAL_DOWNLOAD_FOLDER, filename=title)
    print(f"Audio file downloaded: {title}")

    # Write the file on disk as an MP3 file
    base, ext = os.path.splitext(audio_file)
    mp3_file = base + '.mp3'
    os.rename(audio_file, mp3_file)

    return mp3_file, title

def is_valid_youtube_url(url: str) -> bool:
    """
    purpose: 
        check if the URL is a valid YouTube URL
    input:
        url: YouTube URL
    output:
        True if the URL is a valid YouTube URL, False otherwise
    """

    pattern = r'^(https?\:\/\/)?(www\.youtube\.com|youtu\.?be)\/.+$'
    return re.match(pattern, url)

def cleanup_temp_folder_if_needed() -> None:
    """
    purpose:
        delete files in temp folder if the total size is greater than 1 GB
    input:
        None
    output:
        None
    """

    folder = LOCAL_DOWNLOAD_FOLDER
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

if __name__ == '__main__':
    os.makedirs(LOCAL_DOWNLOAD_FOLDER, exist_ok=True)
    parser = argparse.ArgumentParser(description='Youtube Download')
    parser.add_argument('-p', '--port', type=int, default=13000, help='Specify the port number')
    args = parser.parse_args()
    port = args.port
    app.run(host='0.0.0.0', port=port)
