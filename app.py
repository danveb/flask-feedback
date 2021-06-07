from flask import Flask, render_template, redirect, flash, session
from flask_debugtoolbar import DebugToolbarExtension 
from models import db, connect_db, User, Feedback
from forms import RegisterForm, LoginForm, FeedbackForm
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

# GET & POST /register
@app.route('/register', methods=["GET", "POST"]) 
def register_user():
    if "user_id" in session: 
        return redirect(f"/users/{session['user_id']}")
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
            form.username.errors.append('Username already exists. Please try a new username')
            return render_template('register.html', form=form)
        # ['username'] in session  
        session['user_id'] = new_user.username
        flash('Welcome! Successfully Created Your New Account')
        return redirect(f'/users/{username}') 
    # GET Register Form 
    return render_template('register.html', form=form) 

# GET & POST /login
@app.route('/login', methods=["GET", "POST"]) 
def login_user():
    if "user_id" in session: 
        return redirect(f"/users/{session['user_id']}")
    # LoginForm instance 
    form = LoginForm() 
    if form.validate_on_submit():
        username = form.username.data
        password = form.password.data 
        # call authenticate (classmethod)
        current_user = User.authenticate(username, password) 
        if current_user:
            flash(f'Welcome back, {current_user.username}')
            # ['username'] in session  
            session['user_id'] = current_user.username
            return redirect(f'/users/{current_user.username}')
        else: 
            form.username.errors = ['Invalid username/password. Please retry'] 
    # GET Login Form
    return render_template('login.html', form=form) 

# GET /secret
# @app.route('/secret')
# def show_page():
#     # add username into session; if not in session flash and redirect 
#     if "username" not in session:
#         flash('Please login first')
#         return redirect('/')
#     return render_template('secret.html')

# GET /users/<username>
@app.route('/users/<username>') 
def user_details(username):
    if 'user_id' not in session:
        flash('Please Login first')
        return redirect('/login')
    else: 
        user = User.query.get_or_404(username)
        feedback = Feedback.query.filter_by(username=username)
        return render_template('details.html', user=user, feedback=feedback)

# GET /logout 
@app.route('/logout')
def logout_user():
    # remove user session
    session.pop('user_id')
    flash('Successfully Logged Out')
    return redirect('/login') 

# POST /users/<username>/delete 
@app.route('/users/<username>/delete', methods=["POST"])
def delete_user(username):
    if 'user_id' not in session or username != session['user_id']:
        flash('You Do Not Have Access') 
        return redirect('/')
    user = User.query.get_or_404(username)
    db.session.delete(user)
    db.session.commit()
    session.pop('user_id')
    return redirect('/login')

# GET & POST /users/<username>/feedback/add
@app.route('/users/<username>/feedback/add', methods=["GET", "POST"])
def feedback_form(username):
    if 'user_id' not in session: 
        flash('You Do Not Have Access')
        return redirect('/')
    form = FeedbackForm()
    if form.validate_on_submit():
        title = form.title.data
        content = form.content.data
        new_feedback = Feedback(username=username, title=title, content=content)
        db.session.add(new_feedback)
        db.session.commit() 
        return redirect(f'/users/{username}')
    else: 
        return render_template('feedback.html', form=form) 

# GET & POST /feedback/<int:feedback_id>/update
@app.route('/feedback/<int:feedback_id>/update', methods=["GET", "POST"])
def update_feedback(feedback_id):
    feedback = Feedback.query.get_or_404(feedback_id)
    if 'user_id' not in session: 
        flash('You Do Not Have Access')
        return redirect('/')
    form = FeedbackForm()
    if form.validate_on_submit():
        feedback.title = form.title.data
        feedback.content = form.content.data
        db.session.add(feedback)
        db.session.commit() 
        return redirect(f'/users/{feedback.username}')
    else: 
        return render_template('update_feedback.html', form=form, feedback=feedback) 

# POST /feedback/<int:feedback_id>/delete 
@app.route('/feedback/<int:feedback_id>/delete', methods=["POST"]) 
def delete_feedback(feedback_id):
    feedback = Feedback.query.get_or_404(feedback_id)
    if 'user_id' not in session:
        flash('You Do Not Have Access')
        return redirect('/')
    else:
        db.session.delete(feedback)
        db.session.commit()
    return redirect(f'/users/{feedback.username}')