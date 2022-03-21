from flask import render_template, flash, redirect, url_for, request
from flask_login import login_user, login_required, logout_user, current_user
from . import auth
from .forms import LoginForm, RegistrationForm, UserInformationForm
from .. import db
from ..models import User
from werkzeug.security import generate_password_hash


@auth.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        passw_hash = generate_password_hash(form.password.data)
        user = User(username=form.username.data, email=form.email.data, password_hash=passw_hash)
        if user is not None and user.verify_password(form.password.data):
            login_user(user, form.remember_me.data)
            next = request.args.get('next')
            if next is None or not next.startswith('/'):
                next = url_for('main.index')
            return redirect(next)
        flash('Invalid username or password.')
    return render_template('login.html', form=form)


@auth.route('/logout')
@login_required
def logout():
    logout_user()
    flash('You have been logged out.')
    return redirect(url_for('main.index'))


@auth.route('/register', methods=['GET', 'POST'])
def register():
    form = RegistrationForm()
    if form.validate_on_submit():
        user = User(email=form.email.data,
                username=form.username.data,
                password=form.password.data)
        db.session.add(user)
        db.session.commit()
        flash('You can now Login')
        '''token = user.generate_confirmation_token()
        send_email(user.email, 'Confirm Your Account', 'auth/email/confirm', user=user, token=token)'''
        return redirect(url_for('auth.login'))
    return render_template('register.html', form=form)


'''@auth.route('/confirm/<token>')
@login_required
def confirm(token):
    if current_user.confirmed:
        return redirect(url_for('main.index'))
    if current_user.confirm(token):
        db.session.commit()
        flash('you have confirmed your account. Thanks')
    else:
        flash('The confirmation lin is invalid r has expired.')
    return redirect(url_for('main.index'))


@auth.before_app_request
def before_request():
    if current_user.is_authenticated \
            and not current_user.confirmed \
            and request.blueprint != 'auth' \
            and request.endpoint != 'static':
        return redirect(url_for('auth.unconfirmed'))


@auth.route('/unconfirmed')
def unconfirmed():
    if current_user.is_anoymous or current_user.confirmed:
        return redirect(url_for('main.index'))
    return render_template('unconfirmed.html')'''


@auth.route('/userinfo', methods=['GET', 'POST'])
def userinfo():
    form = UserInformationForm()
    if form.validate_on_submit():
        user = User(firstname=form.firstname.data,
                    lastname=form.lastname.data,
                    birthday=form.birthday.data,
                    personalizedsiganture=form.PersonalizedSignature.data,
                    username=form.username.data)
        db.session.add(user)
        db.session.commit()
        flash("change UserInformation successfully")
    return render_template('userinfo.html',form=form)

