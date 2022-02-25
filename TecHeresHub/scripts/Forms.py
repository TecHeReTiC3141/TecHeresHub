from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, \
    BooleanField, SubmitField, EmailField, DateField
from wtforms.validators import DataRequired

class LoginForm(FlaskForm):
    email = EmailField('Email', validators=[DataRequired()])
    password = PasswordField('Password', validators=[DataRequired()])
    remainme = BooleanField('Remain me')
    submit = SubmitField('Send')


class RegisterForm(FlaskForm):
    name = StringField('Nickname', validators=[DataRequired()])
    birthdate = DateField('Birth')
    email = EmailField('Email', validators=[DataRequired()])
    password = PasswordField('PassWord', validators=[DataRequired()])
    repeat_password = PasswordField('PassWord', validators=[DataRequired()])
    submit = SubmitField('Send')
