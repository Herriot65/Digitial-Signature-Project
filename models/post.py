from extensions import db
from datetime import datetime

class Post(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100), nullable=False)
    content = db.Column(db.Text, nullable=False)
    author_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    created_at=db.Column(db.Date,nullable=False,default=datetime.now())
    token = db.Column(db.String(64), nullable=False, unique=True)
    
    def __repr__(self):
        return '<Post %s>' % self.title