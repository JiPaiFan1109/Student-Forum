from flask_wtf import Form
from wtforms import StringField, PasswordField, BooleanField, SubmitField
from wtforms.validators import InputRequired, Length, Email, Regexp, EqualTo
from wtforms import ValidationError
from ..models import User


class LoginForm(Form):
    username = StringField('User Name', validators=[InputRequired(message='请输入用户名')])
    password = PasswordField('Password', validators=[InputRequired(message='请输入密码')])
    remember_me = BooleanField('remember_me')
    submit = SubmitField('submit')

    def validate_on_submit(self):
        pass


class RegistrationForm(Form):
    email = StringField('Email', validators=[InputRequired(), Length(1, 64),
                                             Email()])
    username = StringField('Username', validators=[
        InputRequired(), Length(1, 64), Regexp('^[A-Za-z][A-Za-z0-9_.]*$', 0,
                                               'Usernames must have only letters,'
                                               'numbers, dots or underscores')])
    password = PasswordField('Password', validators=[
        InputRequired(), EqualTo('password2', message='Password must match.')])
    password2 = PasswordField('Confirm password', validators=[InputRequired()])
    submit = SubmitField('Register')

    def validate_email(self, field):
        if User.query.filter_by(email=field.data).first():
            raise ValidationError('Email already registered.')

    def validate_username(self, field):
        if User.query.filter_by(username=field.data).first():
            raise ValidationError('Username already in use')
    def validate_on_submit(self):
        pass