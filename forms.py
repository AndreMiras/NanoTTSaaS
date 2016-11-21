from wtforms import Form, validators, TextAreaField, SelectField
from wtforms.fields.html5 import DecimalField
from libnanotts import NanoTts


VOICE_CHOICES = [(voice, voice) for voice in NanoTts.get_voices()]


class NanoTtsForm(Form):
    text = TextAreaField(
        u'Text',
        [validators.InputRequired(), validators.length(max=200)],
        default=u"Nano T T S service.")
    voice = SelectField(
                validators=[validators.Optional()],
                choices=VOICE_CHOICES,
                default='en-GB')
    speed = DecimalField(validators=[
                validators.Optional(), validators.NumberRange(0.2, 5.0)])
    pitch = DecimalField(validators=[
                validators.Optional(), validators.NumberRange(0.5, 2.0)])
