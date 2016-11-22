import os
import random
from datetime import datetime, timedelta
from tempfile import NamedTemporaryFile
from flask import Flask, request, render_template, send_from_directory, \
    jsonify, url_for
from forms import TtsApiForm
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


def api_helper(csrf_enabled=True):
    """
    Helper function for handling request and preparing audio download.
    1) Processes the request, extracting form data
    2) Runs nanotts with requested parameters
    3) Returns processed form and audio file
    """
    text = None
    audio_file = None
    response_type = None
    # 1) Processes the request, extracting form data
    form = TtsApiForm(request.form, csrf_enabled=csrf_enabled)
    if request.method == 'POST' and form.validate():
        text = form.text.data
        voice = form.voice.data
        speed = form.speed.data
        pitch = form.pitch.data
        response_type = form.response_type.data
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
        "form": form,
        "text": text,
        "audio_file": audio_file,
        "response_type": response_type,
    }
    return data


@app.route('/api', methods=['POST'])
def api():
    """
    API view, handles the form using the api_helper(),
    then return either:
    1) form errors as json
    2) audio file address
    3) audio file content
    """
    csrf_enabled = False
    data = api_helper(csrf_enabled)
    form = data['form']
    audio_file = data['audio_file']
    response_type = data['response_type']
    # 1) form errors as json
    if form.errors:
        return jsonify(**form.errors)
    # 2) audio file address
    if response_type is not None and response_type == 'audio_address':
        response_dict = {
            "audio_file": url_for('static', filename=audio_file),
        }
        return jsonify(**response_dict)
    # 3) audio file content
    else:
        audio_filename = os.path.basename(audio_file)
        return send_from_directory(audio_directory(), audio_filename)


@app.route('/', methods=['GET', 'POST'])
def home():
    """
    Home view, handles the form using the api_helper().
    Changes the default form response_type value to "audio_address"
    rather than "audio_content".
    """
    data = api_helper()
    form = data['form']
    form.response_type.data = 'audio_address'
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
