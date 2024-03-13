from extensions import db
from datetime import datetime

class Post(db.Model):
    """
    Define the Post model for database representation of posts.

    This class represents the Post model in the database, defining its structure and relationships with other models.

    Attributes:
        id (int): The primary key of the post.
        title (str): The title of the post, limited to 100 characters.
        content (str): The content of the post, stored as text.
        author_id (int): The foreign key referencing the user who authored the post.
        created_at (datetime): The timestamp indicating the creation date of the post.
        token (str): A unique token associated with the post.

    Methods:
        __repr__: Returns a string representation of the post object.
    """
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100), nullable=False)
    content = db.Column(db.Text, nullable=False)
    author_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    created_at=db.Column(db.Date,nullable=False,default=datetime.now())
    token = db.Column(db.String(64), nullable=False, unique=True)
    
    def __repr__(self):
        return '<Post %s>' % self.title