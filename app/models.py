from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.orm import relationship
from passlib.hash import bcrypt
from flask_login import UserMixin
import uuid

db = SQLAlchemy()


class User(UserMixin, db.Model):
    __tablename__ = 'user'

    # single fields
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(127), nullable=False)
    password = db.Column(db.String(127), nullable=False)

    # relationships
    debates = relationship('Debate', back_populates='created_by')

    # basic init
    def __init__(self, username: str, password: str):
        self.username = username
        self.password = bcrypt.encrypt(password)

    def validate_password(self, password):
        return bcrypt.verify(password, self.password)

    def __repr__(self):
        return '<User %r>' % self.username

    def __str__(self):
        return '<User %r>' % self.username


class Debate(db.Model):
    __tablename__ = 'debate'

    # specific stuff
    id = db.Column(db.Integer, primary_key=True)
    url = db.Column(db.String(127), nullable=False)  # url at which the debate is accessed (internal)
    title = db.Column(db.String(127), nullable=False)
    description = db.Column(db.String(127), nullable=True)
    join_password = db.Column(db.String(127), nullable=True)
    active = db.Column(db.Boolean, default=False)  # 0 is locked, 1 is unlocked


    # relationships
    created_by_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    created_by = relationship('User', back_populates='debates')

    def __init__(self, title: str, description: str, password: str):
        self.title = title
        self.description = description
        self.join_password = bcrypt.encrypt(password)

        # generate url
        cur_url = str(uuid.uuid4())[-10:]

        while Debate.query.filter_by(url=cur_url).first() is not None:
            cur_url = str(uuid.uuid4())[-10:]

        self.url = cur_url

    def __repr__(self):
        return "<Debate %s>" % self.url

    def __str__(self):
        return "<Debate %s>" % self.url
