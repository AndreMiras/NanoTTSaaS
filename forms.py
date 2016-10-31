from wtforms import Form, TextAreaField, validators


class NanoTtsForm(Form):
    text = TextAreaField(
        u'Text', [validators.InputRequired(), validators.length(max=200)])
