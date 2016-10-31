import os
import random
from datetime import datetime, timedelta
from tempfile import NamedTemporaryFile
from flask import Flask, request, render_template, flash
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


@app.route('/', methods=['GET', 'POST'])
def home():
    text = None
    audio_file = None
    form = NanoTtsForm(request.form)
    if request.method == 'POST' and form.validate():
        text = form.text.data
        flash('Playing wav.')
        nanotts = NanoTts()
        nanotts.noplay = True
        # TODO: use tempfile module
        f = NamedTemporaryFile(
            suffix=AUDIO_FORMAT, dir=audio_directory(), delete=False)
        f.close()
        audio_file = os.path.join("audio", os.path.basename(f.name))
        nanotts.output = f.name
        nanotts.run(text)
        delete_old_audio_files(audio_directory())
    data = {
        "text": text,
        "audio_file": audio_file,
        "form": form,
    }
    return render_template('home.html', **data)


if __name__ == '__main__':
    secret_key = os.environ.get('SECRET_KEY')
    # generates a one time secret key
    if secret_key is None:
        choice = "abcdefghijklmnopqrstuvwxyz0123456789!@#$%^&*(-_=+)"
        secret_key = "".join([random.choice(choice) for i in range(50)])
    app.secret_key = secret_key
    app.run(port=8000, debug=True)
