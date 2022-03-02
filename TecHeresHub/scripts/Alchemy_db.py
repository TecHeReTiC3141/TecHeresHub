from app import db
from datetime import datetime


class User(db.Model):

    id = db.Column(db.INTEGER, primary_key=True, autoincrement=True)
    name = db.Column(db.String(64), unique=True)
    email = db.Column(db.String(64), unique=True)
    password = db.Column(db.String(128), unique=True, index=True)
    posts = db.relationship('Post', backref='author', lazy='dynamic')

    def __repr__(self):
        return f'<User {self.name}>'


class Post(db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    title = db.Column(db.String(50))
    text = db.Column(db.String(140))
    timestamp = db.Column(db.DateTime, index=True, default=datetime.utcnow)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))

    def __repr__(self):
        return f'<Post {self.title}>'
