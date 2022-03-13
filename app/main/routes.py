from flask import render_template, flash, redirect
from app.main import app
'''from app.main.forms import LoginForm'''


@app.route('/')
@app.route('/index')

def index():
    return 'Hello World!'


'''@app.route('/login')
def login():
    form = LoginForm()
    if form.validate_on_submit():
        flash('用户登录的名户名是:{} , 是否记住我:{}'.format(
            form.username.data, form.remember_me.data))
        return redirect('/index')
    return render_template('login.html', title='登 录', form=form)'''