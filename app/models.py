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

    def to_json(self):
        return {
            'username': self.username,
            'email': self.email,
            'password_hash': self.password_hash
            }

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

    def to_json(self):
        return {
            'id': self.id,
            'character': self.character,
            'metric': self.metric,
            'score': self.score
            }

    def __repr__(self):
        return '<Results {}>'.format(self.character)

class Votes(db.Model):
        id = db.Column(db.Integer, primary_key=True)
        user_id = db.Column(db.Integer)
        alpha_character = db.Column(db.String(140), index=True)
        beta_character = db.Column(db.String(140), index=True)
        metric = db.Column(db.String(140), index=True)

        def __repr__(self):
            return '<Vote {}>'.format(self.id)

        def to_json(self):
            return {
                'id': self.id,
                'user_id': self.user_id,
                'metric': self.metric,
                'alpha_character': self.alpha_character,
                'beta_character': self.beta_character
                }

class Polls(db.Model):
        id = db.Column(db.Integer, primary_key=True)
        user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
        metric = db.Column(db.String(140), db.ForeignKey('results.metric'))

        def to_json(self):
            return {
                'id': self.id,
                'user_id': self.user_id,
                'metric': self.metric,
                }



@login.user_loader
def load_user(id):
    return User.query.get(int(id))
