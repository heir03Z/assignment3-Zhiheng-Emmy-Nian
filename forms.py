from wtforms import Form, StringField, SubmitField, validators


class GeoForm(Form):
    placename = StringField(
        "place name", [validators.DataRequired(), validators.Length(min=3, max=20)]
    )
    submit = SubmitField("Submit")
