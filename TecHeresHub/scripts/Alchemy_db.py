from app import db

class UserBase(db.Model):

    id = db.Column(db.INTEGER, primary_key=True)
    name = db.Column(db.String(64), unique=True)
    email = db.Column(db.String(64), unique=True)
    password = db.Column(db.String(128), unique=True, index=True)

    def __repr__(self):
        return '<User {}>'.format(self.name)
