from flask_wtf import FlaskForm 
from wtforms import StringField, PasswordField # username,password 
from wtforms.validators import InputRequired, Length # for required

# RegisterForm to hold username, password, email, first_name, last_name
class RegisterForm(FlaskForm):
    # fields 
    username = StringField('Username', validators=[InputRequired(), Length(min=1, max=20)])
    password = PasswordField('Password', validators=[InputRequired(), Length(min=5, max=50)])
    email = StringField('Email', validators=[InputRequired(), Length(min=1, max=50)])
    first_name = StringField('First Name', validators=[InputRequired(), Length(min=1, max=30)])
    last_name = StringField('Last Name', validators=[InputRequired(), Length(min=1, max=30)])

# LoginForm to hold username, password, email, first_name, last_name
class LoginForm(FlaskForm):
    # fields 
    username = StringField('Username', validators=[InputRequired()])
    password = PasswordField('Password', validators=[InputRequired()])

# FeedbackForm to hold title, content
class FeedbackForm(FlaskForm):
    # fields 
    title = StringField('Title', validators=[InputRequired()])
    content = StringField('Content', validators=[InputRequired()])