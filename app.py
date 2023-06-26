from __future__ import unicode_literals
import yt_dlp
import os
from pytube import YouTube
from flask import Flask, request, send_file, render_template, redirect, flash, send_from_directory
app = Flask(__name__)
app.secret_key = "your_secret_key"
# import youtube_dl


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
    url = request.form.get("url", None)
    if not url:
        flash('Please enter a valid URL.')
        return render_template('index.html')
    try:
        # try with pytube first
        yt = YouTube(url)
        video = yt.streams.filter(only_audio=True).first()
        out_file = video.download()
        base, ext = os.path.splitext(out_file)
        new_file = base + '.mp3'
        os.rename(out_file, new_file)
        return send_file(new_file, as_attachment=True)

    except Exception as e:
        # if pytube fails, use yt-dlp
        print("Pytube encountered an error, falling back to yt-dlp: ", str(e))
        try:
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
                # Change extension to mp3
                filename = filename.rsplit(".", 1)[0] + ".mp3"
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
            'format': 'bestvideo[ext=mp4][vcodec=avc1]+bestaudio[ext=m4a]/mp4+best[height<=480]'
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


########### pytube version mp3 audio ##############
# @app.route('/download', methods=["POST", "GET"])
# def download_mp3():
#     if request.method == 'POST':
#         url = request.form.get("url", None)
#         if not url:
#             flash('Please enter a valid URL.')
#             return render_template('index.html')
#         try:
#             yt = YouTube(url)
#             video = yt.streams.filter(only_audio=True).first()
#             out_file = video.download()
#             base, ext = os.path.splitext(out_file)
#             new_file = base + '.mp3'
#             os.rename(out_file, new_file)
#             return send_file(new_file,as_attachment=True)
#         except Exception as e:
#             flash(str(e))
#             return render_template('index.html')
#     return render_template('index.html')
