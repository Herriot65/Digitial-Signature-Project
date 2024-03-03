from datetime import datetime
from flask_login import UserMixin
from extensions import db

class User(db.Model, UserMixin):
    """
    :class: `User` represents a user in the system
    :param id: The user's unique ID.
    :param username: The username of the user.
    :param email: The email address of the user.
    :param password_hashed: Hashed password of the user.
    :param confirmed: (optional) Whether the user's email is confirmed.
    :param create_at: (optional) The date of user creation.

    """
    __tablename__ = "users"
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(64), nullable=False)
    email = db.Column(db.String(100), unique=True, nullable=False)
    password_hashed = db.Column(db.String(100), unique=True, nullable=False)
    confirmed = db.Column(db.Boolean, default=False)
    created_at=db.Column(db.Date,nullable=False,default=datetime.now())

    # __repr__ method
    def __repr__(self):
        return '<User %s>' % self.username

