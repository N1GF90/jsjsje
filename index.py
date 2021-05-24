from flask import Flask, render_template, request, send_file
from pytube import YouTube
from os import path
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
        fname = local_download_path.split("//")[-1]
        return send_file(fname, as_attachment=True)

@app.after_request
def after_request(response):
    if request.endpoint == "download":
        global local_download_path
        if path.exists(local_download_path):
            os.remove(local_download_path)
            print("File Removed Succesfully")
    return response