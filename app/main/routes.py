from flask import render_template, flash, redirect, url_for, session
from flask_login import login_required, current_user
from . import main
from .forms import NameForm, EditProfileForm
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
    return render_template('index.html',
                           form=form, name=session.get('name'),
                           known=session.get('know', False))


@main.route('/user/<username>')
def user(username):
    user = User.query.filter_by(usernamne=username).first_or_404()
    return render_template('userinfo.html', user=user)


@main.route('/edit-profile', methods=['GET', 'POST'])
@login_required
def edit_profile():
    form = EditProfileForm()
    if form.validate_on_submit():
        current_user.name = form.name.data
        current_user.location = form.location.data
        current_user.about_me = form.about_me.data
        db.session.add(current_user.get_current_object())
        db.session.commit()
        flash('Your profile has been updated')
        return redirect(url_for('.user', username=current_user.userame))
    form.name.data = current_user.name
    form.location.data = current_user.location
    form.about_me.data = current_user.about_me
    return render_template('edit_profile.html', form=form)














