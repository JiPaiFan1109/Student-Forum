from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, BooleanField, SubmitField, TextAreaField
from wtforms.validators import InputRequired, Length
from flask_pagedown.fields import PageDownField
from wtforms.validators import DataRequired, Length, Email, Regexp, EqualTo


class EditProfileForm(FlaskForm):
    username = StringField('Username', render_kw={'placeholder': 'Username'}, validators=[
        DataRequired(), Length(1, 64), Regexp('^[A-Za-z][A-Za-z0-9_.]*$', 0,
                                              'Usernames must have only letters,'
                                              'numbers, dots or underscores')])
    birthday = StringField('Birthday', render_kw={'placeholder': 'January 1st'},
                           validators=[DataRequired(), Length(1, 64)])
    name = StringField('Real name', render_kw={'placeholder': 'ZhangSan'}, validators=[Length(0, 64)])
    about_me = TextAreaField('About me', render_kw={'placeholder': 'Good'},
                             validators=[DataRequired(), Length(0, 500)])
    institute = StringField('Institute', render_kw={'placeholder': 'None'}, validators=[DataRequired(), Length(1, 64)])
    submit = SubmitField('Save Changes')
    Upload = SubmitField('Change Portrait')

'''
    PersonalizedSignature = TextAreaField('PersonalizedSignature', render_kw={'placeholder': 'Good'},
                                          validators=[DataRequired(), Length(0, 500)])
    submit = SubmitField('save changes')
    UploadPortrait = SubmitField('change portrait')'''


class SearchForm(FlaskForm):
    text = TextAreaField('What are u looking for?', validators=[DataRequired()])
    submit = SubmitField('Search')


class PostForm(FlaskForm):
    title = TextAreaField('Change your title here:', validators=[DataRequired()])
    body = PageDownField('Change your post here:', validators=[DataRequired()])
    submit = SubmitField('Submit')


class CommentForm(FlaskForm):
    body = StringField('', validators=[DataRequired()])
    submit = SubmitField('Submit')


class AnnouncementForm(FlaskForm):
    title = TextAreaField('Enter the title of the Announcement', validators=[DataRequired()])
    body = PageDownField('Enter the content of the Announcement', validators=[DataRequired()])
    submit = SubmitField('Submit')

