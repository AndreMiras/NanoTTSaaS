import os
import random
from datetime import datetime, timedelta
from tempfile import NamedTemporaryFile
from flask import Flask, request, render_template, send_from_directory, \
    jsonify
from forms import NanoTtsForm
from libnanotts import NanoTts

app = Flask(__name__)
AUDIO_FORMAT = ".wav"


def audio_directory():
    """
    Returns the audio directory absolute path.
    """
    return os.path.join(app.static_folder, 'audio')


def delete_old_audio_files(path, hours=24):
    """
    Looks in `path` for files older than `hours`
    and delete them.
    """
    for filename in os.listdir(path):
        if filename.endswith(AUDIO_FORMAT):
            filepath = os.path.join(path, filename)
            file_modified = datetime.fromtimestamp(os.path.getmtime(filepath))
            if datetime.now() - file_modified > timedelta(hours=hours):
                os.remove(filepath)


@app.route('/favicon.ico')
def favicon():
    return send_from_directory(
            os.path.join(app.root_path, 'static', 'img'),
            'favicon.ico', mimetype='image/vnd.microsoft.icon')


def api_helper():
    """
    Helper function for handling request and preparing audio download.
    1) Processes the request, extracting form data
    2) Runs nanotts with requested parameters
    3) Returns processed form and audio file
    """
    text = None
    audio_file = None
    # 1) Processes the request, extracting form data
    form = NanoTtsForm(request.form)
    if request.method == 'POST' and form.validate():
        text = form.text.data
        voice = form.voice.data
        speed = form.speed.data
        pitch = form.pitch.data
        # 2) Runs nanotts with requested parameters
        nanotts = NanoTts()
        nanotts.noplay = True
        nanotts.voice = voice
        nanotts.speed = speed
        nanotts.pitch = pitch
        f = NamedTemporaryFile(
            suffix=AUDIO_FORMAT, dir=audio_directory(), delete=False)
        f.close()
        audio_file = os.path.join("audio", os.path.basename(f.name))
        nanotts.output = f.name
        nanotts.run(text)
        delete_old_audio_files(audio_directory())
    # 3) Returns processed form and audio file
    data = {
        "text": text,
        "audio_file": audio_file,
        "form": form,
    }
    return data


@app.route('/api', methods=['POST'])
def api():
    data = api_helper()
    form = data['form']
    audio_file = data['audio_file']
    if form.errors:
        return jsonify(**form.errors)
    audio_filename = os.path.basename(audio_file)
    return send_from_directory(audio_directory(), audio_filename)


@app.route('/', methods=['GET', 'POST'])
def home():
    data = api_helper()
    return render_template('home.html', **data)


def setup():
    secret_key = os.environ.get('SECRET_KEY')
    # generates a one time secret key
    if secret_key is None:
        choice = "abcdefghijklmnopqrstuvwxyz0123456789!@#$%^&*(-_=+)"
        secret_key = "".join([random.choice(choice) for i in range(50)])
    app.secret_key = secret_key
setup()

if __name__ == '__main__':
    app.run(port=8000, debug=True)
