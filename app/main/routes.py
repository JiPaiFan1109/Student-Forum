from datetime import datetime

from flask import render_template, flash, redirect, url_for, session, abort, request, current_app, make_response
from flask_login import login_required, current_user
from . import main
from .forms import EditProfileForm, PostForm, AnnouncementForm, \
    CommentForm, SearchForm, ChangeAvatarForm
from .. import db
from ..decorators import permission_required
from ..models import User, Permission, Post, Category
from ..models import User, Permission, Post, Comment, Announcement


@main.route('/', methods=['GET', 'POST'])
def index():
    form = PostForm()
    content = ''
    if form.validate_on_submit() and \
            current_user.can(Permission.WRITE):
        category_id = form.category_id.data
        categories = Category.query.get(category_id)
        if not categories:
            flash('There is no such category, please check the number.')
        post = Post(title=form.title.data,
                    body=form.body.data,
                    categoriy_id=form.category_id.data,
                    author=current_user._get_current_object(),
                    moment=datetime.now().strftime('%Y-%m-%d %H:%M:%S'))
        post.categories = categories.name
        db.session.add(post)
        return redirect(url_for('.index'))
    sform = SearchForm()
    if sform.validate_on_submit():
        content = sform.text.data
    page = request.args.get('page', 1, type=int)
    show_followed = False
    if current_user.is_authenticated:
        show_followed = bool(request.cookies.get('show_followed', ''))
    if show_followed:
        query = current_user.followed_posts
    else:
        query = Post.query
    pagination = query.filter(Post.title.like('%' + content + '%')).order_by(Post.timestamp.desc()).paginate(
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
                           moment=datetime.now().strftime('%Y-%m-%d %H:%M:%S')
                           # author=current_user._get_current_object()
                           )
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


@main.route('/ucomments/<username>', methods=['GET', 'POST'])
def ucomments(username):
    user = User.query.filter_by(username=username).first()
    if user is None:
        abort(404)
    page = request.args.get('page', 1, type=int)
    pagination = user.comments.order_by(Comment.timestamp.desc()).paginate(
        page, per_page=current_app.config['FLASK_COMMENTS_PER_PAGE'],
        error_out=False)
    comments = pagination.items
    return render_template('ucomments.html', user=user, comments=comments,
                           pagination=pagination)


@main.route('/edit-profile', methods=['GET', 'POST'])
@login_required
def edit_profile():
    form = EditProfileForm()
    aform = ChangeAvatarForm()
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
    if aform.validate_on_submit():
        avatar = request.files['avatar']
        fname = avatar.filename
        upload_folder = current_app.config['UPLOAD_FOLDER']
        allowed_extensions = ['png', 'jpg', 'jpeg', 'gif']
        fext = fname.rsplit('.', 1)[-1] if '.' in fname else ''
        if fext not in allowed_extensions:
            flash('Please check if its one of png, '
                  'jpg, jpeg and gif')
            return redirect(url_for('main.edit_profile',
                                    username=current_user.username))
        target = '{}{}.{}'.format(upload_folder, current_user.username, fext)
        avatar.save(target)
        current_user.real_avatar = '/static/avatars/{}.{}'.format(current_user.username, fext)
        db.session.add(current_user)
        flash('Your avatar has been updated.')
        return redirect(url_for('main.edit_profile', username=current_user.username))
    form.username.data = current_user.username
    form.birthday.data = current_user.birthday
    form.name.data = current_user.name
    form.about_me.data = current_user.about_me
    form.institute.data = current_user.institute
    username = current_user.username
    return render_template('userinfo.html', aform=aform, form=form, username=username, user=current_user)


@main.route('/follow/<username>')
@login_required
@permission_required(Permission.FOLLOW)
def follow(username):
    user = User.query.filter_by(username=username).first()
    if user is None:
        flash('Invalid user.')
        return redirect(url_for('.index'))
    if current_user.is_following(user):
        flash('You are already following this user.')
        return redirect(url_for('.user', username=username))
    current_user.follow(user)
    db.session.commit()
    flash('You are now following %s.' % username)
    return redirect(url_for('.user', username=username))


@main.route('/unfollow/<username>')
@login_required
@permission_required(Permission.FOLLOW)
def unfollow(username):
    user = User.query.filter_by(username=username).first()
    if user is None:
        flash('Invalid user.')
        return redirect(url_for('.index'))
    if not current_user.is_following(user):
        flash('You are not following this user.')
        return redirect(url_for('.user', username=username))
    current_user.unfollow(user)
    db.session.commit()
    flash('You are not following %s anymore.' % username)
    return redirect(url_for('.user', username=username))


@main.route('/followers/<username>')
def followers(username):
    user = User.query.filter_by(username=username).first()
    if user is None:
        flash('Invalid user. ')
        return redirect(url_for(' .index'))
    page = request.args.get('page', 1, type=int)
    pagination = user.followers.paginate(
        page, per_page=current_app.config['FLASKY_FOLLOWERS_PER_PAGE'],
        error_out=False)
    follows = [{'user': item.follower, 'timestamp': item.timestamp}
               for item in pagination.items]
    return render_template('followers.html', user=user, title="Followers of",
                           endpoint='.followers', pagination=pagination,
                           follows=follows)


@main.route('/followed_by/<username>')
def followed_by(username):
    user = User.query.filter_by(username=username).first()
    if user is None:
        flash('Invalid user.')
        return redirect(url_for('.index'))
    page = request.args.get('page', 1, type=int)
    pagination = user.followed.paginate(
        page, per_page=current_app.config['FLASKY_FOLLOWERS_PER_PAGE'],
        error_out=False)
    follows = [{'user': item.followed, 'timestamp': item.timestamp}
               for item in pagination.items]
    return render_template('followers.html', user=user, title="Followed by",
                           endpoint='.followed_by', pagination=pagination,
                           follows=follows)


@main.route('/all')
@login_required
def show_all():
    resp = make_response(redirect(url_for('.index')))
    resp.set_cookie('show_followed', '', max_age=30 * 24 * 60 * 60)
    return resp


@main.route('/followed')
@login_required
def show_followed():
    resp = make_response(redirect(url_for('.index')))
    resp.set_cookie('show_followed', '1', max_age=30 * 24 * 60 * 60)
    return resp


@main.route('/post/<int:id>', methods=['GET', 'Post'])
def post(id):
    post = Post.query.get_or_404(id)
    post.read_count += 1
    comment_count = post.comments.count()
    form = CommentForm()
    if form.validate_on_submit():
        comment = Comment(body=form.body.data,
                          post=post,
                          author=current_user._get_current_object(),
                          moment=datetime.now().strftime('%Y-%m-%d %H:%M:%S'))
        db.session.add(comment)
        db.session.commit()
        flash('Your comment has been published')
        return redirect(url_for('.post', id=post.id, page=-1, user=current_user))
    page = request.args.get('page', 1, type=int)
    if page == -1:
        page = (post.comments.count() - 1) // \
               current_app.config['FLASKY_COMMENTS_PER_PAGE'] + 1
    pagination = post.comments.order_by(Comment.timestamp.desc()).paginate(
        page, per_page=current_app.config['FLASKY_COMMENTS_PER_PAGE'],
        error_out=False)
    comments = pagination.items
    return render_template('post.html', posts=[post], form=form,
                           comments=comments, pagination=pagination, user=current_user, comment_count=comment_count)


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

#
# @main.route('/change-avatar', methods=['GET', 'POST'])
# @login_required
# def change_avatar():
#     form = ChangeAvatarForm()
#     if aform.avatar.data is not None:
#         avatar = request.files['avatar']
#         fname = avatar.filename
#         upload_folder = current_app.config['UPLOAD_FOLDER']
#         allowed_extensions = ['png', 'jpg', 'jpeg', 'gif']
#         fext = fname.rsplit('.', 1)[-1] if '.' in fname else ''
#         if fext not in allowed_extensions:
#             flash('Please check if its one of png, '
#                   'jpg, jpeg and gif')
#             return redirect(url_for('main.edit_profile',
#                                     username=current_user.username))
#         target = '{}{}.{}'.format(upload_folder, current_user.username, fext)
#         avatar.save(target)
#         current_user.real_avatar = '/static/avatars/{}.{}'.format(current_user.username, fext)
#         db.session.add(current_user)
#         flash('Your avatar has been updated.')
#         return redirect(url_for('main.edit_profile', username=current_user.username))
#     return render_template('userinfo.html', form=form, username=current_user.username)
