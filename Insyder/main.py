# from flask import Flask, render_template, request,url_for,redirect,flash,send_from_directory,session
# from werkzeug.security import generate_password_hash,check_password_hash
# from flask_login import UserMixin,LoginManager,login_user,login_required,current_user,logout_user
# from flask_wtf import FlaskForm
# from wtforms import StringField,PasswordField,SubmitField
# from wtforms.validators import DataRequired, Email
# from flask_sqlalchemy import SQLAlchemy
# from sqlalchemy import create_engine


# app = Flask(__name__)


# # CONFIGURE FLASK-APP TO USE FLASK-LOGIN 
# # table creation in the DATABASE
# login_manager = LoginManager()
# login_manager.init_app(app)

# # configuring the table
# @login_manager.user_loader
# def user_loader(user_id):
#     return User.query.get(int(user_id))




# # CREATING INSYDER DATABASE
# app.config['SQLALCHEMY_DATABASE_URI'] = "sqlite:///insyder.db"
# app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
# db = SQLAlchemy(app)
# engine = create_engine("mysql+pymysql://user:pw@host/db", pool_pre_ping=True)


# #CREATING A DATABASE(TABLE) FOR THE REGISTRATION(SIGN UP) PROCESS
# # registeration table
# class User(UserMixin,db.Model):
#     __tablename__ = 'users'
#     id = db.Column(db.Integer,nullable=False, primary_key=True)
#     firstname = db.Column(db.String(40), nullable = False)
#     lastname = db.Column(db.String(40), nullable = False)
#     email = db.Column(db.String(40),nullable = False, primary_key=True, unique=True)
#     password = db.Column(db.String(30),nullable=False)
# db.session.autoflush = True
# db.create_all()


# # new_user = User(firstname="",lastname="",email="",password="")
# # db.session.add(new_user)
# # db.session.commit()

# # THE SECRET KEY TO ACTIVATE WTFORM
# app.secret_key = "My-Name-is"

# # INDEX ROUTE
# @app.route("/")
# def index_page():
#     return render_template("home.html")



# # REGISTER FORM INHERITANCE
# # form for the registration process
# class RegisterForm(FlaskForm):
#     firstname = StringField(label='Firstname',validators=[DataRequired()])
#     lastname = StringField(label='Lastname',validators=[DataRequired()])
#     email = StringField(label='Email',validators=[DataRequired()])
#     password = PasswordField(label='Password',validators=[DataRequired()])
#     submit = SubmitField(label='Register')

# #REGISTER ROUTE
# @app.route('/register', methods=["GET", "POST"])
# def register_page():
#     form = RegisterForm()
#     if form.validate_on_submit():

#         if User.query.filter_by(email=form.email.data).first():
#             print(User.query.filter_by(email=form.email.data).first())
#             #User already exists
#             flash("You've already signed up with that email, log in instead!")
#             return redirect(url_for('login_page'))

#         hash_and_salted_password = generate_password_hash(
#             form.password.data,
#             method='pbkdf2:sha256',
#             salt_length=8
#         )
#         new_user = User(
#             firstname=form.firstname.data,
#             lastname=form.lastname.data,
#             email=form.email.data,
           
#             password=hash_and_salted_password,
#         )
#         db.session.add(new_user)
#         db.session.commit()
#         db.session.flush()
#         login_user(new_user)
#         return redirect(url_for("secrets_page"))

#     return render_template("register.html", form=form, current_user=current_user)





# # LOGIN FORM INHERITANCE
# # form for the login process
# class LoginForm(FlaskForm):
#     email = StringField(label='Email', validators=[DataRequired()])
#     password = PasswordField(label= 'Password',validators=[DataRequired()])
#     submit = SubmitField(label='Log In')

# # LOGIN ROUTE
# @app.route('/login', methods=["GET", "POST"])
# def login_page():
#     form = LoginForm()
#     if form.validate_on_submit():
#         email = form.email.data
#         password = form.password.data

#         user = User.query.filter_by(email=email).first()
#         # Email doesn't exist or password incorrect.
#         if not user:
#             flash("That email does not exist, please try again.")
#             return redirect(url_for('login_page'))
#         elif not check_password_hash(user.password, password):
#             flash('Password incorrect, please try again.')
#             return redirect(url_for('login_page'))
#         else:
#             login_user(user)
#             return redirect(url_for('secrets_page'))
#     return render_template("login.html", form=form, current_user=current_user)

     
# @app.route("/secrets")
# @login_required
# def secrets_page():
#     print(current_user.firstname)
#     return render_template("welcome.html", name=current_user.firstname ,current_user=current_user)



    
# if __name__ == "__main__":
#     app.run(debug=True)

# https://python.plainenglish.io/implementing-flask-login-with-hash-password-888731c88a99

from flask import Flask, render_template, request,url_for,redirect,flash,send_from_directory
from werkzeug.security import generate_password_hash,check_password_hash
from flask_login import UserMixin,LoginManager,login_user,login_required,current_user,logout_user
from flask_wtf import FlaskForm
from flask_bootstrap import Bootstrap
from wtforms import StringField,PasswordField,SubmitField
from flask_wtf.file import FileField, FileRequired, FileAllowed
from wtforms.validators import DataRequired, Email
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import create_engine
from flask_ckeditor import CKEditor, CKEditorField
from datetime import date
from sqlalchemy.orm import relationship
from flask_gravatar import Gravatar


app = Flask(__name__)


# CONFIGURE FLASK-APP TO USE FLASK-LOGIN 
# table creation in the DATABASE
login_manager = LoginManager()
login_manager.init_app(app)

# configuring the table
@login_manager.user_loader
def user_loader(user_id):
    return User.query.get(int(user_id))




# CREATING INSYDER DATABASE
app.config['SQLALCHEMY_DATABASE_URI'] = "sqlite:///insyder.db"
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)
ckeditor = CKEditor(app)
Bootstrap(app)
gravatar = Gravatar(app, size=100, rating='g', default='retro', force_default=False, force_lower=False, use_ssl=False, base_url=None)
engine = create_engine("mysql+pymysql://user:pw@host/db", pool_pre_ping=True)


#CREATING A DATABASE(TABLE) FOR THE REGISTRATION(SIGN UP) PROCESS
# registeration table
class User(UserMixin,db.Model):
    __tablename__ = "users"
    id = db.Column(db.Integer, primary_key=True)
    firstname = db.Column(db.String(40), nullable = False)
    lastname = db.Column(db.String(40), nullable = False)
    email = db.Column(db.String(40),nullable = False, unique=True)
    password = db.Column(db.String(30),nullable=False)
    posts = relationship("BlogPost", back_populates='author')
    comments = relationship("Comment", back_populates='comment_author')


# Blog Tables
class BlogPost(db.Model):
    __tablename__ = "blogposts"
    id = db.Column(db.Integer, primary_key=True)
    author_id = db.Column(db.Integer, db.ForeignKey("users.id"))
    author = relationship("User", back_populates="posts")
    title = db.Column(db.String(250),unique=True,nullable=False)
    body = db.Column(db.Text,nullable=False)
    date = db.Column(db.String(250),nullable=False)
    # author = db.Column(db.String(250),nullable=False)
    # img = db.Column(db.LargeBinary)
    comments = relationship("Comment", back_populates='parent_post')


# comment Tables
class Comment(db.Model):
    __tablename__ = "comments"
    id = db.Column(db.Integer, primary_key=True)
    post_id = db.Column(db.Integer, db.ForeignKey("blogposts.id"))
    author_id = db.Column(db.Integer, db.ForeignKey("users.id"))
    parent_post = relationship("BlogPost", back_populates="comments")
    comment_author = relationship("User", back_populates="comments")
    text = db.Column(db.Text,nullable=False)

# create all tables(users,blogposts,comments)    
db.create_all()




# new_user = User(firstname="",lastname="",email="",password="")
# db.session.add(new_user)
# db.session.commit()

# THE SECRET KEY TO ACTIVATE WTFORM
app.secret_key = "My-Name-is"

# INDEX ROUTE
@app.route("/")
def index_page():
    return render_template("home.html")



# REGISTER FORM INHERITANCE
# form for the registration process
class RegisterForm(FlaskForm):
    firstname = StringField(label='Firstname',validators=[DataRequired()])
    lastname = StringField(label='Lastname',validators=[DataRequired()])
    email = StringField(label='Email',validators=[DataRequired()])
    password = PasswordField(label='Password',validators=[DataRequired()])
    submit = SubmitField(label='Register')

#REGISTER ROUTE
@app.route("/register",methods=["POST","GET"])
def register_page():

    form = RegisterForm()
    # register_form.validate_on_submit()
   

    if request.method == "POST":
        # TO CHECK IF RECORDS ALREADY IN DATABASE
        if User.query.filter_by(email=request.form.get('email')).first():
            flash("You've already Signed up with that email,Please log in Instead")
            return redirect(url_for('login_page'))

        # HASHING AND SALTING FOR AUTHENTICATION
        hash_and_salted_password = generate_password_hash(
            request.form.get('password'),
            method = 'pbkdf2:sha256',
            salt_length = 8


        )
        # GETTING THE NEW_USER TO THE DATABADE 
        new_user = User(
            firstname = request.form.get('firstname'),
            lastname = request.form.get('lastname'),
            email = request.form.get('email'),
            password = hash_and_salted_password
        )
        db.session.add(new_user)
        db.session.commit()
        db.session.flush()


        login_user(new_user)
        return redirect(url_for('display_post'))

    return render_template('register.html',form=form, logged_in=current_user.is_authenticated)







# LOGIN FORM INHERITANCE
# form for the login process
class LoginForm(FlaskForm):
    email = StringField(label='Email', validators=[DataRequired()])
    password = PasswordField(label= 'Password',validators=[DataRequired()])
    submit = SubmitField(label='Log In')

# LOGIN ROUTE
@app.route("/login", methods=["POST","GET"])
def login_page():

    login_form = LoginForm()
    login_form.validate_on_submit()
    form=login_form



    if request.method == 'POST':
        email = request.form.get('email')
        password = request.form.get('password')
        # CHECK FOR ERROR
        user = User.query.filter_by(email=email).first()
        # IF USER(NAME) IS INCORRECT
        if not user:
            flash("That email does not exist,Please try again")
            return redirect(url_for('login_page'))
            # PASSWORD INCORRECT
        elif not check_password_hash(user.password,password):
            flash("Incorrect Passord,Please Enter Correct Password")
            return redirect(url_for('login_page'))
            # BOTH ARE CORRECT
        else:
            login_user(user)
            return redirect(url_for('display_post'))
            
        
    return render_template("login.html", login_form = LoginForm(), form=login_form, logged_in=current_user.is_authenticated)

     
@app.route("/secrets")
@login_required
def secrets_page():
    print(current_user.firstname)
    return render_template("welcome.html", name=current_user.firstname ,logged_in=True)



# wtforms for posts
class PostForm(FlaskForm):
    title = StringField(label='Title',validators=[DataRequired()])
    body = CKEditorField(label='Post',validators=[DataRequired()])
    author = StringField(label='Your Name',validators=[DataRequired()])
    # img = FileField(validators=[FileRequired()])
    submit = SubmitField(label='Submit Post')

class CommentForm(FlaskForm):
    comment_text = CKEditorField(label='Comment', validators=[DataRequired()])
    submit = SubmitField(label='Submit Comment')



@app.route("/post/<int:post_id>", methods=["GET", "POST"])
def show_post(post_id):
    form = CommentForm()
    requested_post = BlogPost.query.get(post_id)

    if form.validate_on_submit():
        if not current_user.is_authenticated:
            flash("You need to login or register to comment.")
            return redirect(url_for("login_page"))

        new_comment = Comment(
            text=form.comment_text.data,
            comment_author=current_user,
            parent_post=requested_post
        )
        db.session.add(new_comment)
        db.session.commit()

    return render_template("posts.html", post=requested_post, form=form, current_user=current_user)

# New Post route
@app.route("/new-post", methods=["GET","POST"])
def add_new_post():
    form = PostForm()
    if form.validate_on_submit():
        new_post = BlogPost(
            title = request.form.get('title'),
            body = request.form.get('body'),
            author = current_user,
            # img = request.form.get('img'),
            date = date.today().strftime("%B %d, %Y"),
        )
        db.session.add(new_post)
        db.session.commit()
        return redirect(url_for("display_post"))
    return render_template("make-post.html", form=form, current_user=current_user)

# Edit Post Route
@app.route("/edit-post/<int:post_id>", methods=["GET", "POST"])
def edit_post(post_id):
    post = BlogPost.query.get(post_id)
    edit_form = PostForm(
        title = post.title,
        body = post.body,
        author = current_user,
        # img = post.img

    )
    if edit_form.validate_on_submit():
        post.title = edit_form.title.data
        post.body = edit_form.body.data
        # post.img = edit_form.img.data
        db.session.commit()
        return redirect(url_for('show_post', post_id=post_id))
    return render_template("make-post.html", form=edit_form, is_edit=True, current_user=current_user)

@app.route("/delete-post/<int:post_id>")
def delete_post(post_id):
    post_to_delete = BlogPost.query.get(post_id)
    db.session.delete(post_to_delete)
    db.session.commit()
    return redirect(url_for('display_post'))


@app.route("/logout")
def logout():
    logout_user()
    return redirect(url_for('index_page'))


@app.route("/display")
def display_post():
    posts = BlogPost.query.all()
    return render_template("mainpage.html",all_posts=posts, current_user=current_user)

    
if __name__ == "__main__":
    app.run(debug=True)

# https://python.plainenglish.io/implementing-flask-login-with-hash-password-888731c88a99