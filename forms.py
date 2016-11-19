from wtforms import Form, validators, TextAreaField, SelectField
from libnanotts import NanoTts


class NanoTtsForm(Form):
    text = TextAreaField(
        u'Text',
        [validators.InputRequired(), validators.length(max=200)],
        default=u"Nano T T S service.")
    voice = SelectField(
        choices=[(voice, voice) for voice in NanoTts.get_voices()])
