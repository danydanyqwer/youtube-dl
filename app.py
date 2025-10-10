from flask import Flask, render_template, request, abort, send_file
from pytubefix import YouTube
from pytubefix.cli import on_progress
import tempfile
import os



app = Flask(__name__)

@app.route('/', methods = ['POST', 'GET'])
def index():
    if request.method == 'POST':
        link = request.form.get("linkyoutube")
        linkExtension = request.form.get("extensions").lower()
        yt = YouTube(link, on_progress_callback=on_progress)

        with tempfile.TemporaryDirectory() as tmpdir:
            filepath = os.path.join(tmpdir, f"{yt.title}.{linkExtension}")

        if linkExtension == 'mp4':
            ys = yt.streams.filter(progressive=True, file_extension="mp4").order_by('resolution').desc().first()
            if not ys:
                return abort(400, "No progressive stream available")
            ys.download(output_path=tmpdir, filename=f"{yt.title}.mp4")
        elif linkExtension == 'm4a':
            ys = yt.streams.get_audio_only()
            ys.download(output_path=tmpdir, filename=f"{yt.title}.m4a")
        else:
            return abort(400, "Unsupported format")

        return send_file(filepath, as_attachment=True)

        return render_template('index.html')
    else:
        return render_template('index.html')
    

    

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=False)

