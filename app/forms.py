# Add any form classes for Flask-WTF here
from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, FileField, TextAreaField
from wtforms.validators import InputRequired,Email
from flask_wtf.file import FileField, FileAllowed, FileRequired



class LoginForm(FlaskForm):
    username = StringField('Username', validators=[InputRequired()])
    password = PasswordField('Password', validators=[InputRequired()])

class RegistrationForm(FlaskForm):
    username = StringField('Username', validators=[InputRequired()])
    password = PasswordField('Password', validators=[InputRequired()])
    firstname = StringField('Firstname', validators=[InputRequired()])
    lastname = StringField('Lastname', validators=[InputRequired()])
    email = StringField('Email', validators=[InputRequired(), Email()])
    location = StringField('Location', validators=[InputRequired()])
    biography = TextAreaField('Biography', validators=[InputRequired()])
    photo = FileField('Photo', validators=[
        FileRequired(),
        FileAllowed(["jpg", "jpeg", "png"], "Only images"),
    ],
    )

class PostForm(FlaskForm):
    photo = FileField('Photo', validators=[
        FileRequired(),
        FileAllowed(["jpg", "jpeg", "png"], 'Images only!')])
    caption = TextAreaField('Caption', validators=[InputRequired()])


