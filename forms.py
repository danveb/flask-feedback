from flask_wtf import FlaskForm 
from wtforms import StringField, PasswordField # username,password 
from wtforms.validators import InputRequired # for required

# RegisterForm to hold username, password, email, first_name, last_name
class RegisterForm(FlaskForm):
    # fields 
    username = StringField('Username', validators=[InputRequired()])
    password = PasswordField('Password', validators=[InputRequired()])
    email = StringField('Email', validators=[InputRequired()])
    first_name = StringField('First Name', validators=[InputRequired()])
    last_name = StringField('Last Name', validators=[InputRequired()])

# LoginForm to hold username, password, email, first_name, last_name
class LoginForm(FlaskForm):
    # fields 
    username = StringField('Username', validators=[InputRequired()])
    password = PasswordField('Password', validators=[InputRequired()])