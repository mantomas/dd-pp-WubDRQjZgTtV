from flask_wtf import FlaskForm
from flask_wtf.file import FileField, FileAllowed
from wtforms import (
    StringField,
    DateTimeField,
    SubmitField,
    TextAreaField,
)
from wtforms import HiddenField
from wtforms import validators
from wtforms.validators import DataRequired, Length
from config import Config


class AddForm(FlaskForm):
    title = StringField("Title", validators=[DataRequired(), Length(max=140)])
    desc = TextAreaField("Description", validators=[Length(min=0, max=500)])
    deadline = DateTimeField(
        "DD.MM.YYYY HH:MM", validators=[validators.optional()], format="%d.%m.%Y %H:%M"
    )
    upload_file = FileField(
        "Optional attachment",
        validators=[validators.optional(), FileAllowed(Config.FILE_ALLOWED)],
    )
    time_offset = HiddenField("time_offset")
    submit = SubmitField("Submit")
