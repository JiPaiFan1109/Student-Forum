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


class PostForm(FlaskForm):
    title = TextAreaField('Change your title here:', validators=[InputRequired()])
    # body = TextAreaField('Change your post here:', validators=[InputRequired()])
    body = PageDownField('Change your post here:', validators=[InputRequired()])
    submit = SubmitField('Submit')
    '''index 的route处理这个表单然后把以前发布的博客列表传给模板'''
