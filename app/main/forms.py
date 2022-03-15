from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, BooleanField, SubmitField
from wtforms.validators import InputRequired


class NameForm:
    name = StringField('What is your name?', validators=[InputRequired()])
    submit = SubmitField('Submit')

    def validate_on_submit(self):
        pass