from __future__ import unicode_literals
from flask import Flask, request, send_file, render_template, redirect, flash, send_from_directory
app = Flask(__name__)
app.secret_key = "your_secret_key"
from pytube import YouTube
import os
import yt_dlp
import youtube_dl

@app.route('/')
def home():
	return render_template('index.html')

@app.route('/about')
def about():
	return render_template('about.html')

@app.route('/terms-conditions')
def terms():
	return render_template('terms-conditions.html')

@app.route('/download', methods=["POST", "GET"])
def download_mp3():
    try:
        url = request.form.get("url", None)
        if not url:
            flash('Please enter a valid URL.')
            return render_template('index.html')

        ydl_opts = {
            'outtmpl': 'downloads/%(title)s.%(ext)s',
            'format': 'bestaudio/best',
            'postprocessors': [{
                'key': 'FFmpegExtractAudio',
                'preferredcodec': 'mp3',
                'preferredquality': '192',
            }],
        }
        
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            info_dict = ydl.extract_info(url, download=True)
            filename = ydl.prepare_filename(info_dict)
            filename = filename.rsplit(".", 1)[0] + ".mp3"  # Change extension to mp3
            return send_from_directory('downloads', os.path.basename(filename), as_attachment=True)
    except Exception as e:
        flash(str(e))
        return render_template('index.html')




@app.route('/downloadvid', methods=["POST", "GET"])
def download_video():
    try:
        url = request.form.get("url", None)
        if not url:
            flash('Please enter a valid URL.')
            return render_template('index.html')

        ydl_opts = {
            'outtmpl': 'downloads/%(title)s.%(ext)s',
            'format': 'bestvideo[ext=mp4]+bestaudio[ext=m4a]/best[ext=mp4]/best'
        }
        
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            info_dict = ydl.extract_info(url, download=True)
            filename = ydl.prepare_filename(info_dict)
            return send_from_directory('downloads', os.path.basename(filename), as_attachment=True)
    except Exception as e:
        flash(str(e))
        return render_template('index.html')

if __name__ == '__main__':
	app.run(port=5000, debug=True)
