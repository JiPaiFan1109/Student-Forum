from flask import render_template, flash, redirect, url_for, session, abort, request, current_app
from flask_login import login_required, current_user
from . import main
from .forms import EditProfileForm, PostForm, AnnouncementForm, CommentForm, SearchForm
from .. import db
from ..models import User, Permission, Post, Comment, Announcement


@main.route('/', methods=['GET', 'POST'])
def index():
    form = PostForm()
    content = ''
    if form.validate_on_submit() and \
            current_user.can(Permission.WRITE):
        post = Post(title=form.title.data,
                    body=form.body.data,
                    author=current_user._get_current_object())
        db.session.add(post)
        return redirect(url_for('.index'))
    sform = SearchForm()
    if sform.validate_on_submit():
        content = 'aaa'
        print('inininininiininininininininininininininininin')
    print(content, '++++++++++++++++++++++++++++++++++++++++++++++++++++')
    page = request.args.get('page', 1, type=int)
    pagination = Post.query.filter(Post.title.like('%' + content + '%')).order_by(Post.timestamp.asc()).paginate(
        page, per_page=current_app.config['FLASK_POSTS_PER_PAGE'],
        error_out=False)
    posts = pagination.items
    return render_template('index.html', form=form, sform=sform, posts=posts, pagination=pagination)


@main.route('/announcement', methods=['GET', 'POST'])
@login_required
def announcement():
    form = AnnouncementForm()
    if form.validate_on_submit():
        ann = Announcement(title=form.title.data,
                           body=form.body.data,
                           author=current_user._get_current_object())
        db.session.add(ann)
        return redirect(url_for('.announcement'))
    page = request.args.get('page', 1, type=int)
    pagination = Announcement.query.order_by(Announcement.timestamp.desc()).paginate(
        page, per_page=current_app.config['FLASK_ANNOUNCEMENT_PER_PAGE'],
        error_out=False)
    announcements = pagination.items
    return render_template('announcement.html', form=form, announcements=announcements,
                           pagination=pagination)


@main.route('/user/<username>', methods=['GET', 'POST'])
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
    page = request.args.get('page', 1, type=int)
    if page == -1:
        page = (post.comments.count() - 1) // \
            current_app.config['FLASKY_COMMENTS_PER_PAGE'] + 1
    pagination = post.comments.order_by(Comment.timestamp.asc()).paginate(
        page, per_page=current_app.config['FLASKY_COMMENTS_PER_PAGE'],
        error_out=False)
    comments = pagination.items
    return render_template('post.html', posts=[post], form=form,
                           comments=comments, pagination=pagination)


@main.route('/edit/<int:id>', methods=['GET', 'POST'])
@login_required
def edit(id):
    post = Post.query.get_or_404(id)
    if current_user != post.author and \
            not current_user.can(Permission.ADMINISTER):
        abort(403)
    form = PostForm()
    if form.validate_on_submit():
        post.title = form.title.data
        post.body = form.body.data
        db.session.add(post)
        flash('The post has been updated.')
        return redirect(url_for('main.index'))
        # return redirect(url_for('post', id=post.id))
    form.title.data = post.title
    form.body.data = post.body
    return render_template('edit_post.html', form=form)

