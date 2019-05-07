from datetime import datetime
from app import db, login
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import UserMixin
from sqlalchemy.ext.hybrid import hybrid_property
from sqlalchemy import select, func

class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(64), index=True, unique=True)
    email = db.Column(db.String(120), index=True, unique = True)
    password_hash = db.Column(db.String(128))
    posts = db.relationship('Post', backref='author', lazy='dynamic')

    def __repr__(self):
        return '<User {}>'.format(self.username)

    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)

class Post(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    body = db.Column(db.String(140))
    timestamp = db.Column(db.DateTime, index=True, default=datetime.utcnow)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))

    def __repr__(self):
        return '<Post {}>'.format(self.body)

class Results(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    character = db.Column(db.String(140))
    metric = db.Column(db.String(140))
    score = db.Column(db.Integer)

    def __repr__(self):
        return '<Results {}>'.format(self.character)

class Votes(db.Model):
        id = db.Column(db.Integer, primary_key=True)
        user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
        alpha_character = db.Column(db.String(140), db.ForeignKey('results.character'))
        beta_character = db.Column(db.String(140), db.ForeignKey('results.character'))
        metric = db.Column(db.String(140), db.ForeignKey('results.metric'))

class Polls(db.Model):
        id = db.Column(db.Integer, primary_key=True)
        user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
        metric = db.Column(db.String(140), db.ForeignKey('results.metric'))



@login.user_loader
def load_user(id):
    return User.query.get(int(id))
