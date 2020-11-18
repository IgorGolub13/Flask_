from flask import render_template, url_for, flash, redirect, request
from app import app, db, bcrypt
from app.forms import RegistrationForm, LoginForm, UpdateAccountForm, AddPost, UpdatePost
from app.models import User, Post
from flask_login import login_user, current_user, logout_user, login_required
from werkzeug.urls import url_parse
import os
import secrets
from PIL import Image
from datetime import datetime as dt


@app.route('/')
def index():
    return render_template('index.html', name='Прикладна математика',
                           title='PNU')


# @app.route('/secret')
# @login_required
# def secret():
#     return 'Only authenticate users are allowed!'


@app.route('/post/<int:id>')
def dynamic_post(id):
    post = Post.query.filter_by(id=id).first()
    return render_template("post.html", post=post)

@app.route('/delete_post/<int:id>')
def delete_post(id):
    post = Post.query.filter_by(id=id).first()
    db.session.delete(post)
    db.session.commit()
    return redirect(url_for('posts'))


@app.route('/posts/add_post', methods=['GET', 'POST'])
def add_post():
    form = AddPost()
    if form.validate_on_submit():
        title = form.title.data
        content = form.content.data
        user_id = current_user.id
        date_posted = dt.utcnow()
        post = Post(title=title, content=content, user_id=user_id, date_posted = date_posted)
        db.session.add(post)
        db.session.commit()
        flash('New post added!', category='success')
        return redirect(url_for('posts'))
    return render_template('add_post.html', form = form)

@app.route('/posts/update_post', methods=['GET', 'POST'])
def update_post():
    form = UpdatePost()
    if form.validate_on_submit():
        current_user.title = form.title.data
        current_user.content = form.content.data
        current_user.user_id = current_user.id
        current_user.date_posted = dt.utcnow()
        db.session.commit()
        flash('Your post updated!', category='success')
        return redirect(url_for('posts'))
    return render_template('update_post.html', form = form)

@app.route("/register", methods=['GET', 'POST'])
def register():
    if current_user.is_authenticated:
        return redirect(url_for('index'))
    form = RegistrationForm()
    if form.validate_on_submit():
        # user = User.query.filter_by(email=form.email.data).first()
        # if user:
        #     flash(f'Акаунт вже існує {form.email.data}!', category='warning')
        #     return redirect(url_for('register'))
        # 2. зберегти дані з БД
        username = form.username.data
        email = form.email.data
        password_hash = form.password.data
        user = User(username=username, email=email, password=bcrypt.generate_password_hash(password_hash))
        db.session.add(user)
        db.session.commit()
        flash(f'Account created for {form.username.data}!', category='success')
        return redirect(url_for('login'))
    return render_template('registration.html', title='Register', form=form)


@app.route("/login", methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('index'))
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        if user and bcrypt.check_password_hash(user.password, form.password.data):
            login_user(user, remember=form.remember.data)
            flash('You have been logged in!', category='success')
            next_page = request.args.get("next")
            if not next_page or url_parse(next_page).netloc != '':
                next_page = url_for('index')
            return redirect(next_page)
        flash('Login unsuccessful. Please check username and password', category='warning')
        return redirect(url_for('login'))
    return render_template('login.html', form=form, title='Login')


@app.route('/logout')
def logout():
    logout_user()
    flash('You have been logged out')
    return redirect(url_for('index'))


@app.before_request
def before_request():
    if current_user.is_authenticated:
        current_user.last_seen = dt.utcnow()
        db.session.commit()


@app.route('/account', methods=['GET', 'POST'])
@login_required
def account():
    form = UpdateAccountForm()
    if form.validate_on_submit():
        if form.picture.data:
            picture_file = save_picture(form.picture.data)
            current_user.image_file = picture_file
        current_user.username = form.username.data
        current_user.email = form.email.data
        current_user.about_me = form.about_me.data
        current_user.password = bcrypt.generate_password_hash(form.password.data)
        db.session.commit()
        flash(f'Account update for {form.username.data}!', category='success')
        return redirect(url_for('account'))
    elif request.method == 'GET':
        form.username.data = current_user.username
        form.email.data = current_user.email
    image_file = url_for('static', filename='image/' + current_user.image_file)
    return render_template('account.html', title="Account", image_file=image_file, form=form)


@app.route('/posts', methods=['GET', 'POST'])
def posts():
    posts = Post.query.all()
    return render_template("posts.html", title='Home', posts=posts)


def save_picture(form_picture):
    random_hex = secrets.token_hex(8)
    f_name, f_ext = os.path.splitext(form_picture.filename)
    picture_fn = random_hex + f_ext
    picture_path = os.path.join(app.root_path, 'static/image', picture_fn)

    output_size = (250, 250)
    i = Image.open(form_picture)
    i.thumbnail(output_size)
    i.save(picture_path)

    return picture_fn
