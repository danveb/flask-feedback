from flask import Flask, render_template, redirect, session, flash
from flask_debugtoolbar import DebugToolbarExtension 
from models import db, connect_db, User 
from forms import RegisterForm, LoginForm
# exceptions for creating duplicate username
from sqlalchemy.exc import IntegrityError

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql:///flask_feedback'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False 
app.config['SQLALCHEMY_ECHO'] = True 
app.config['SECRET_KEY'] = 'benitocamela'
app.config['DEBUG_TB_INTERCEPT_REDIRECTS'] = False 

# createdb 
connect_db(app)
db.create_all() 

toolbar = DebugToolbarExtension(app)

# GET / 
@app.route('/')
def home():
    return redirect('/register') 

# GET /register & POST /register
@app.route('/register', methods=["GET", "POST"]) 
def register_user():
    # RegisterForm instance 
    form = RegisterForm()
    if form.validate_on_submit():
        # get form data back 
        username = form.username.data 
        password = form.password.data 
        email = form.email.data
        first_name = form.first_name.data
        last_name = form.last_name.data 
        # instance (classmethod) 
        # error handling later where username could be duplicated and we want to prevent that
        new_user = User.register(username, password, email, first_name, last_name)

        # db
        db.session.add(new_user)
        try:
            db.session.commit()
        except IntegrityError:
            form.username.errors.append('Username already exists. Please register a new username')
            return render_template('register.html', form=form)
        flash('Welcome! Successfully Created Your New Account')
        return redirect('/secret') 
    # GET Register Form 
    return render_template('register.html', form=form) 

# GET /login & POST /login 
@app.route('/login', methods=["GET", "POST"]) 
def login_user():
    # LoginForm instance 
    form = LoginForm() 
    if form.validate_on_submit():
        username = form.username.data
        password = form.password.data 
        # call authenticate (classmethod)
        new_user = User.authenticate(username, password) 
        if new_user:
            flash(f'Welcome back, {new_user.username}')
            return redirect('/secret')
        else: 
            form.username.errors = ['Invalid username/password. Please retry'] 
    # GET Login Form
    return render_template('login.html', form=form) 

# GET /secret
@app.route('/secret')
def show_page():
    return render_template('secret.html')