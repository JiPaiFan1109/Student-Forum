from flask import render_template, flash, redirect, url_for, session
from . import main
from .forms import NameForm
from .. import db
from ..models import User


@main.route('/', methods=['GET', 'POST'])
def index():
    form = NameForm()
    if form.validate_on_submit():
        old_name = session.get('name')
        if old_name is not None and old_name != form.name.data:
            flash('Looks like you have changed your name!')
        session["name"] = form.name.data
        return redirect(url_for('index'))
    return render_template('frontindex.html',
                           form=form, name=session.get('name'),
                           known=session.get('know', False))


@main.route('/user/<username>')
def user(username):
    user = User.query.filter_by(usernamne=username).first_or_404()
    return render_template('userinfo.html', user=user)
















