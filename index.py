from flask import Flask, render_template, request, send_file
from pytube import YouTube
from os import path
import io
import os

app = Flask(__name__)

local_download_path = None

@app.route('/')
def home():
    return render_template('home.html')

@app.route('/downloadVideo', methods=['POST'])
def download():
    global local_download_path
    if request.method == 'POST':
        downloadLink = request.form['downloadURL']
        local_download_path = YouTube(downloadLink).streams.filter(progressive=True, file_extension='mp4').get_highest_resolution().download()
        #Here we are storing the downloaded file in memory so that we can delete it later from the OS
        return_data = io.BytesIO()
        with open(local_download_path, 'rb') as fo:
            return_data.write(fo.read())
        # (after writing, cursor will be at last byte, so move it to start)
        return_data.seek(0)
        os.remove(local_download_path)
        return send_file(return_data, mimetype='video/mp4',  attachment_filename='download_video.mp4', as_attachment=True)