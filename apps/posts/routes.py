from flask import Blueprint,request,render_template, redirect,flash,url_for
from models.user import User
from models.post import Post
from datetime import datetime
from forms.forms import CreatePostForm,EditPostForm
from flask_login import login_required,current_user
import secrets
from extensions import db

post=Blueprint('posts',__name__,url_prefix='/post')

@login_required
@post.route('/create_post', methods=['GET', 'POST'])
def create_post():
    form=CreatePostForm()
    if form.validate_on_submit():
        title=form.title.data
        content=form.content.data
        author_id=current_user.id
        
        while True:
            token = secrets.token_urlsafe(32)
            if not Post.query.filter_by(token=token).first():
                break
        
        new_post=Post(title=title,content=content,author_id=author_id,created_at=datetime.now(),token=token)
        db.session.add(new_post)
        db.session.commit()
        flash("Your post has been successfully created")
        return redirect(url_for('posts.list_posts'))
    return render_template('create_post.html',form=form)

@post.route('/posts')
@login_required
def list_posts():
    posts = Post.query.all()  
    if not posts:
        flash("You have not made any posts yet.")
    return render_template('posts_list.html', posts=posts)

@login_required
@post.route('/posts/<string:post_token>/edit', methods=['GET', 'POST'])
def edit_post(post_token):
    form = EditPostForm()
    post = Post.query.filter_by(token=post_token).first()
    
    if post:
        if form.validate_on_submit():
            post.title = form.title.data
            post.content = form.content.data
            db.session.commit()
            return redirect(url_for('posts.list_posts'))
        else:
            flash('Post not found')
    
    return render_template('edit_post.html', form=form,post=post)


@login_required
@post.route('/posts/<string:post_token>/delete_post', methods=['POST'])
def delete_post(post_token):
    post = Post.query.filter_by(token=post_token).first()
    
    if not post:
        flash("The post you want to delete does not exist")
        return redirect(url_for('posts.list_posts'))
    else:
        return redirect(url_for('posts.confirm_post_deletion', post_token=post_token))


@login_required
@post.route('/confirm_post_deletion/<string:post_token>', methods=['GET', 'POST'])
def confirm_post_deletion(post_token):
    post = Post.query.filter_by(token=post_token).first()

    if not post:
        flash("The post you want to delete does not exist")
        return redirect(url_for('posts.list_posts'))

    if request.method == 'POST':
        db.session.delete(post)
        db.session.commit()
        return redirect(url_for('posts.list_posts'))

    return render_template('delete_post.html', post=post)

    

