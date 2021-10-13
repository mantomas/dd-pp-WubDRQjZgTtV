from flask_wtf import FlaskForm
from flask_wtf.file import FileField, FileAllowed
from wtforms import (
    StringField,
    BooleanField,
    PasswordField,
    DateTimeField,
    SubmitField,
    TextAreaField,
)
from wtforms import HiddenField
from wtforms import validators
from wtforms.validators import DataRequired, EqualTo, ValidationError, Length
from app.models import User
from config import Config


class LoginForm(FlaskForm):
    username = StringField("Username", validators=[DataRequired()])
    password = PasswordField("Password", validators=[DataRequired()])
    remember_me = BooleanField("Remember Me")
    submit = SubmitField("Log In")


class RegistrationForm(FlaskForm):
    username = StringField("Username", validators=[DataRequired()])
    password = PasswordField("Password", validators=[DataRequired()])
    password2 = PasswordField(
        "Repeat Password", validators=[DataRequired(), EqualTo("password")]
    )
    submit = SubmitField("Register")

    def validate_username(self, username):
        user = User.query.filter_by(username=username.data).first()
        if user is not None:
            raise ValidationError("Use different username.")


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
