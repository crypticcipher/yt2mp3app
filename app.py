from __future__ import unicode_literals
from flask import Flask, request, send_file, render_template, redirect
app = Flask(__name__)
from pytube import YouTube
import os
import youtube_dl

# ydl_opts = {
#     'format': 'bestaudio/best',
#     'postprocessors': [{
#     'key': 'FFmpegExtractAudio',
#     'preferredcodec': 'mp3',
#     'preferredquality': '192',
#     }],
# }


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
	url = request.form["url"]
	print("Someone just tried to download", url)

	yt = YouTube(url)

	video = yt.streams.filter(only_audio=True).first()

	out_file = video.download()

	base, ext = os.path.splitext(out_file)
	new_file = base + '.mp3'
	os.rename(out_file, new_file)

	return send_file(new_file,as_attachment=True)



@app.route('/downloadvid', methods=["POST", "GET"])
def download_video():
    url = request.form["url"]
    print("Someone just tried to download", url)
    with youtube_dl.YoutubeDL() as ydl:
        url = ydl.extract_info(url, download=False)
        print(url)
        try:
            download_link = url["entries"][-1]["formats"][-1]["url"]
        except:
            download_link = url["formats"][-1]["url"]
        return redirect(download_link+"&dl=1")



if __name__ == '__main__':
	app.run(port=5000)
	
# port=5000, debug=True



