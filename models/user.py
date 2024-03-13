from datetime import datetime
from flask_login import UserMixin
from extensions import db

class User(db.Model, UserMixin):
    """
    Define the User model for database representation of users.

    This class represents the User model in the database, defining its structure and attributes.

    Attributes:
        id (int): The primary key of the user.
        username (str): The username of the user, limited to 64 characters.
        email (str): The email address of the user, unique and limited to 100 characters.
        password_hashed (str): The hashed password of the user, stored securely.
        confirmed (bool): Flag indicating whether the user's email address is confirmed.
        created_at (datetime): The timestamp indicating the creation date of the user.

    Methods:
        __repr__: Returns a string representation of the user object.
    """
    __tablename__ = "users"
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(64), nullable=False)
    email = db.Column(db.String(100), unique=True, nullable=False)
    password_hashed = db.Column(db.String(100), unique=True, nullable=False)
    confirmed = db.Column(db.Boolean, default=False)
    created_at=db.Column(db.Date,nullable=False,default=datetime.now())   

    def __repr__(self):
        return '<User %s>' % self.username

