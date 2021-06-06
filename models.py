from flask_sqlalchemy import SQLAlchemy 
from flask_bcrypt import Bcrypt 

db = SQLAlchemy() 
bcrypt = Bcrypt() 

def connect_db(app):
    """Connect to database"""
    db.app = app
    db.init_app(app) 

# User Class 
class User(db.Model):
    __tablename__ = 'users'
    username = db.Column(db.String(20), primary_key=True)
    password = db.Column(db.Text, nullable=False)
    email = db.Column(db.String(50), nullable=False, unique=True)
    first_name = db.Column(db.String(30), nullable=False)
    last_name = db.Column(db.String(30), nullable=False)

    # classmethod (register) -> Flask-Bcrypt
    @classmethod
    def register(cls, username, password, email, first_name, last_name):
        """Register user with hashed password & return user"""
        # turn password into a hash with bcrypt (returns a bytestring)
        hashed = bcrypt.generate_password_hash(password)
        # turn bytestring into normal (unicode utf8) string to store in database
        hashed_utf8 = hashed.decode('utf8')
        # return instance of user with username and hashed pwd 
        return cls(username=username, password=hashed_utf8, email=email, first_name=first_name, last_name=last_name) 

    # classmethod (authenticate) -> Flask-Bcrypt 
    @classmethod
    def authenticate(cls, username, password):
        """Validate that user exists & pwd is correct
        Return user if valid; else return False 
        """
        user = User.query.filter_by(username=username).first() 
        if user and bcrypt.check_password_hash(user.password, password):
            # return user instance 
            return user
        else: 
            return False 