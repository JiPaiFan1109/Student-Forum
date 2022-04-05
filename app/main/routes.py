from flask import render_template, flash, redirect, url_for, session, abort
from flask_login import login_required, current_user
from . import main
from .forms import EditProfileForm, PostForm
from .. import db
from ..models import User, Permission, Post


@main.route('/', methods=['GET', 'POST'])
def index():
    form = PostForm()
    # if current_user.can(Permission.WRITE) and \
    #         form.validate_on_submit():
    if form.validate_on_submit():
        post = Post(title=form.title.data,
                    body=form.body.data,
                    author=current_user._get_current_object())
        db.session.add(post)
        return redirect(url_for('.index'))
    posts = Post.query.order_by(Post.timestamp.desc()).all()
    return render_template('index.html', form=form, posts=posts)


'''同理要和userinfo连起来，这里提供用户的帖子记录posts'''
@main.route('/user/<username>')
def user(username):
    user = User.query.filter_by(username=username).first()
    if user is None:
        abort(404)
    posts = user.posts.order_by(Post.timestamp.desc()).all()
    return render_template('user.html', user=user, posts=posts)


'''要和userinfo连起来，把对应的数据显示到对应位置，这里提供数据库里对应的数据物体'''
@main.route('/edit-profile', methods=['GET', 'POST'])
@login_required
def edit_profile():
    form = EditProfileForm()
    print(form.validate_on_submit(), '+++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++')
    print(form.username.errors)
    print(form.birthday.errors)
    print(form.institute.errors)
    print(form.about_me.errors)
    print(form.name.errors)
    if form.validate_on_submit():
        current_user.username = form.username.data
        current_user.birthday = form.birthday.data
        current_user.name = form.name.data
        current_user.about_me = form.about_me.data
        current_user.institute = form.institute.data
        db.session.add(current_user._get_current_object())
        db.session.commit()
        flash('Your profile has been updated')
        return redirect(url_for('main.edit_profile', username=current_user.username))
    form.username.data = current_user.username
    form.birthday.data = current_user.birthday
    form.name.data = current_user.name
    form.about_me.data = current_user.about_me
    form.institute.data = current_user.institute
    return render_template('userinfo.html', form=form)














