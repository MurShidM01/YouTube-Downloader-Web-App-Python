from flask import Flask, render_template, request, redirect, send_file
from pytube import YouTube
import os

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/download', methods=['POST'])
def download():
    url = request.form['url']
    format_type = request.form['format']

    try:
        yt = YouTube(url)
        
        if format_type == 'mp4':
            video = yt.streams.get_highest_resolution()
            file_path = video.download()
            file_name = file_path.split('/')[-1]
        elif format_type == 'mp3':
            audio = yt.streams.filter(only_audio=True).first()
            file_path = audio.download()
            file_name = file_path.split('/')[-1]
            file_name = file_name.replace('.webm', '.mp3')

        return redirect('/downloaded/' + file_name)
    except Exception as e:
        return render_template('index.html', error=str(e))

@app.route('/downloaded/<filename>')
def downloaded(filename):
    return send_file(filename, as_attachment=True)

if __name__ == '__main__':
    app.run(debug=True)
