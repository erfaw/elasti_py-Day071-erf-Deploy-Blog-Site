from datetime import date
from typing import List
from flask import Flask, abort, render_template, redirect, url_for, flash
from flask_bootstrap import Bootstrap5
from flask_ckeditor import CKEditor
# from flask_gravatar import Gravatar
from flask_login import UserMixin, login_user, LoginManager, current_user, logout_user, login_required
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.orm import relationship, DeclarativeBase, Mapped, mapped_column
from sqlalchemy import Integer, String, Text, ForeignKey
from sqlalchemy.exc import IntegrityError
from functools import wraps
from werkzeug.security import generate_password_hash, check_password_hash
from forms import CreatePostForm, RegisterForm, LoginForm, CommentForm
from dotenv import load_dotenv
from pathlib import Path
import os
from functools import wraps

ROOT_DIR = Path(__file__).resolve().parent
(ROOT_DIR / 'instance').mkdir(exist_ok=True)
db_path = (ROOT_DIR / 'instance' / 'posts.db').as_posix()

load_dotenv(ROOT_DIR/'.env')

app = Flask(__name__)
app.config['SECRET_KEY'] = os.environ.get('SECRET_KEY')
ckeditor = CKEditor(app)
app.config['CKEDITOR_PKG_TYPE'] = 'full'
Bootstrap5(app)

login_manager = LoginManager()
login_manager.init_app(app)

class Base(DeclarativeBase):
    pass
app.config['SQLALCHEMY_DATABASE_URI'] = f'sqlite:///{db_path}'
db = SQLAlchemy(model_class=Base)
db.init_app(app)

class BlogPost(db.Model):
    __tablename__ = "blog_posts"
    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    title: Mapped[str] = mapped_column(String(250), unique=True, nullable=False)
    subtitle: Mapped[str] = mapped_column(String(250), nullable=False)
    date: Mapped[str] = mapped_column(String(250), nullable=False)
    body: Mapped[str] = mapped_column(Text, nullable=False)
    author_id: Mapped[int] = mapped_column(ForeignKey("user.id"))
    author = relationship("User", back_populates="posts")
    img_url: Mapped[str] = mapped_column(String(250), nullable=False)
    comments: Mapped[List["Comment"]] = relationship(back_populates= "post")

class User(UserMixin, db.Model):
    id: Mapped[int] = mapped_column(primary_key= True)
    email: Mapped[str] = mapped_column(String(300), nullable= False, unique= True,)
    password: Mapped[str] = mapped_column(nullable= False)
    name: Mapped[str] = mapped_column(String(300), nullable= False,)
    posts: Mapped[List["BlogPost"]] = relationship(back_populates= "author")
    comments: Mapped[List["Comment"]] = relationship(back_populates= "comment_author")
    def __repr__(self):
        return f"<User object: id={self.id}, email={self.email}, name={self.name}>"
    def to_dict(self):
        return {column.name: getattr(self, column.name) for column in self.__table__.columns}
    
class Comment(db.Model):
    __tablename__ = "comments"
    id: Mapped[int] = mapped_column(primary_key=True)
    text: Mapped[str] = mapped_column(Text, nullable= False)
    user_id = mapped_column(ForeignKey("user.id"))
    comment_author: Mapped[User] = relationship(back_populates= "comments")
    post_id = mapped_column(ForeignKey("blog_posts.id"))
    post: Mapped[BlogPost] = relationship(back_populates= "comments")

    def __repr__(self):
        return f"<Comment object: >"
    def to_dict(self):
        return {column.name: getattr(self, column.name) for column in self.__table__.columns}

with app.app_context():
    db.create_all()

def admin_only(func):
    @wraps(func)
    @login_required 
    def wrapper(*args, **kwargs):
        if current_user.id == 1:
            return func(*args, **kwargs)
        else:
            return abort(403)
    return wrapper

@app.route('/register', methods= ["POST", "GET"])
def register():
    register_form= RegisterForm()
    if register_form.validate_on_submit():
        new_user = User(
            email = register_form.email.data,
            password = generate_password_hash(
                password= register_form.password.data,
                method= 'pbkdf2',
                salt_length= 8,
            ),
            name = register_form.name.data
        )
        try: 
            db.session.add(new_user)
            db.session.commit()
        except IntegrityError as e:
            flash("This email registered already, please try to Login instead.")
            return redirect(url_for('login'))
        flash("User registered Successfully!")
        return redirect(url_for('get_all_posts'))
    return render_template("register.html", form= register_form)

@app.route('/login', methods= ["POST", "GET"])
def login():
    login_form= LoginForm()
    if login_form.validate_on_submit():
        user= db.session.execute(db.select(User).where(User.email == login_form.email.data)).scalar_one_or_none()
        if user and check_password_hash(user.password, login_form.password.data):
            if login_user(user):
                flash(f"Successfully logged in as {user.name}")
                return redirect(url_for('get_all_posts'))
            else: 
                return "There is a Problem!"
        else:
            if not user:
                flash("Email or Password is incorrect! please try again.")
            else: 
                flash("Password is incorrect! please try again.")
            return redirect(url_for('login'))
    return render_template("login.html", form= login_form)

@app.route('/logout')
@login_required
def logout():
    logout_user()
    flash("User succussfully logged out.")
    return redirect(url_for('get_all_posts'))

@app.route('/')
def get_all_posts():
    result = db.session.execute(db.select(BlogPost))
    posts = result.scalars().all()
    return render_template("index.html", all_posts=posts)

@app.route("/post/<int:post_id>", methods= ["POST", "GET"])
def show_post(post_id):
    comment_form = CommentForm()
    requested_post = db.get_or_404(BlogPost, post_id)
    if comment_form.validate_on_submit():
        if not current_user.is_authenticated:
            flash("You need to login first in order to submit a comment.")
            return redirect(url_for('login'))
        new_comment = Comment(
            text= comment_form.user_comment.data,
            comment_author= current_user,
            post= requested_post,
        )
        db.session.add(new_comment)
        db.session.commit()
        flash("Thanks for your Comment!")
        return redirect(
            url_for('show_post', post_id= post_id)
        )
    return render_template("post.html", post=requested_post, form= comment_form)

@app.route("/new-post", methods=["GET", "POST"])
@admin_only
def add_new_post():
    form = CreatePostForm()
    if form.validate_on_submit():
        new_post = BlogPost(
            title=form.title.data,
            subtitle=form.subtitle.data,
            body=form.body.data,
            img_url=form.img_url.data,
            author=current_user,
            date=date.today().strftime("%B %d, %Y")
        )
        db.session.add(new_post)
        db.session.commit()
        return redirect(url_for("get_all_posts"))
    return render_template("make-post.html", form=form)

@app.route("/edit-post/<int:post_id>", methods=["GET", "POST"])
@admin_only
def edit_post(post_id):
    post = db.get_or_404(BlogPost, post_id)
    edit_form = CreatePostForm(
        title=post.title,
        subtitle=post.subtitle,
        img_url=post.img_url,
        author=post.author,
        body=post.body
    )
    if edit_form.validate_on_submit():
        post.title = edit_form.title.data
        post.subtitle = edit_form.subtitle.data
        post.img_url = edit_form.img_url.data
        post.author = current_user
        post.body = edit_form.body.data
        db.session.commit()
        return redirect(url_for("show_post", post_id=post.id))
    return render_template("make-post.html", form=edit_form, is_edit=True)

@app.route("/delete/<int:post_id>")
@admin_only
def delete_post(post_id):
    post_to_delete = db.get_or_404(BlogPost, post_id)
    db.session.delete(post_to_delete)
    db.session.commit()
    return redirect(url_for('get_all_posts'))

@app.route("/about")
def about():
    return render_template("about.html")

@app.route("/contact")
def contact():
    return render_template("contact.html")

@login_manager.user_loader
def load_user(user_id):
    return db.get_or_404(User, user_id)

if __name__ == "__main__":
    app.run(debug=True, port=5002)
