from flask_sqlalchemy import SQLAlchemy
from passlib.hash import bcrypt
from flask_login import UserMixin

db = SQLAlchemy()


class User(UserMixin, db.Model):

    # single fields
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(127), nullable=False)
    password = db.Column(db.String(127), nullable=False)

    # basic init
    def __init__(self, username: str, password: str):
        self.username = username
        self.password = bcrypt.encrypt(password)

    def validate_password(self, password):
        return bcrypt.verify(password, self.password)

    def __repr__(self):
        return '<User %r>' % self.email

    def __str__(self):
        return '<User %r>' % self.email
