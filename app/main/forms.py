from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, BooleanField, SubmitField, TextAreaField
from wtforms.validators import DataRequired, InputRequired, Length
from flask_pagedown.fields import PageDownField

class EditProfileForm(FlaskForm):
    name = StringField('Real name', validators=[Length(0, 64)])
    location = StringField('Location', validators=[Length(0, 64)])
    about_me = TextAreaField('About me')
    submit = SubmitField('Submit')


class PostForm(FlaskForm):
    body = TextAreaField('Post whatever you want?', validators=[InputRequired()])
    submit = SubmitField('Submit')
    '''index 的route处理这个表单然后把以前发布的博客列表传给模板'''

class CommentForm(FlaskForm):
    body = StringField('Enter your comment', validators=[DataRequired()])
    submit = SubmitField('Submit')