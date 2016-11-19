from wtforms import Form, validators, TextAreaField, SelectField, FloatField
from libnanotts import NanoTts


class NanoTtsForm(Form):
    text = TextAreaField(
        u'Text',
        [validators.InputRequired(), validators.length(max=200)],
        default=u"Nano T T S service.")
    voice = SelectField(
        choices=[(voice, voice) for voice in NanoTts.get_voices()])
    speed = FloatField(validators=[
                validators.Optional(), validators.NumberRange(0.2, 5.0)])
    pitch = FloatField(validators=[
                validators.Optional(), validators.NumberRange(0.5, 2.0)])
