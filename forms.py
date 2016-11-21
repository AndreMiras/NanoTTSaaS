from flask_wtf import FlaskForm as Form
from wtforms import validators, TextAreaField, SelectField, StringField
from wtforms.fields.html5 import DecimalField
from wtforms.widgets import HiddenInput
from libnanotts import NanoTts


VOICE_CHOICES = [(voice, voice) for voice in NanoTts.get_voices()]
RESPONSE_TYPE_CHOICES = [
    ("audio_content", "Audio content"),
    ("audio_address", "Audio address"),
]


class NanoTtsForm(Form):
    """
    Gives access to common nanotts options through a form.
    """
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


class TtsApiForm(NanoTtsForm):
    """
    Gives access to NanoTtsForm fields plus more advanced API related fields.
    """
    response_type = StringField(
        # validators=[validators.Optional()],
        default='audio_content',
        widget=HiddenInput(),
        description="Defines if the API should return the audio file itself" +
        "or its address.")

    def validate_response_type(form, field):
        """
        Verifies response_type is a valid choice.
        """
        response_types = [x[0] for x in RESPONSE_TYPE_CHOICES] + ['', '']
        if field.data not in response_types:
            raise validators.ValidationError(
                'Invalid choice %s, must be one of %s' %
                (field.data, response_types))
