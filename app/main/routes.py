from flask import render_template, flash, redirect, url_for, session, abort, request, current_app
from flask_login import login_required, current_user
from . import main
from .forms import EditProfileForm, PostForm, CommentForm
from .. import db
from ..models import User, Permission, Post, Comment


@main.route('/', methods=['GET', 'POST'])
def index():
    form = PostForm()
    if form.validate_on_submit() and \
            current_user.can(Permission.WRITE):
        post = Post(title=form.title.data,
                    body=form.body.data,
                    author=current_user._get_current_object())
        db.session.add(post)
        return redirect(url_for('.index'))
    page = request.args.get('page', 1, type=int)
    pagination = Post.query.order_by(Post.timestamp.desc()).paginate(
        page, per_page=current_app.config['FLASK_POSTS_PER_PAGE'],
        error_out=False)
    posts = pagination.items
    return render_template('index.html', form=form, posts=posts,
                           pagination=pagination)


@main.route('/user/<username>')
def user(username):
    user = User.query.filter_by(username=username).first()
    if user is None:
        abort(404)
    page = request.args.get('page', 1, type=int)
    pagination = user.posts.order_by(Post.timestamp.desc()).paginate(
        page, per_page=current_app.config['FLASK_POSTS_PER_PAGE'],
        error_out=False)
    posts = pagination.items
    return render_template('user.html', user=user, posts=posts,
                           pagination=pagination)


@main.route('/edit-profile', methods=['GET', 'POST'])
@login_required
def edit_profile():
    form = EditProfileForm()
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
    username = current_user.username
    return render_template('userinfo.html', form=form, username=username)

@main.route('/post/<int:id>', methods=['GET', 'Post'])
def post(id):
    post = Post.query.get_or_404(id)
    form = CommentForm()
    if form.validate_on_submit():
        comment = Comment(body=form.body.data,
                          post=post,
                          author=current_user._get_current_object())
        db.session.add(comment)
        db.session.commit()
        flash('Your comment has been published')
        return redirect(url_for('.post', id=post.id, page=-1))














