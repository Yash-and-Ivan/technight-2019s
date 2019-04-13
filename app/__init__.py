from config import *
from flask import Flask, render_template
from flask_migrate import Migrate
from flask_login import LoginManager
from flask_session import Session
from app.models import db, User
from app.routes.main import main
from app.routes.user import user

import pymysql
pymysql.install_as_MySQLdb()

app = Flask(__name__)
app.secret_key = SECRET_KEY
app.config['SECRET_KEY'] = SECRET_KEY
app.config['SESSION_TYPE'] = SESSION_TYPE

# database
app.config['SQLALCHEMY_DATABASE_URI'] = DATABASE_URI
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = SQLALCHEMY_TRACK_MODIFICATIONS

db.init_app(app)

with app.app_context():
    db.create_all()

# other stuff
migrate = Migrate(app, db)
session = Session(app)

# login
login_manager = LoginManager()
login_manager.init_app(app)


@login_manager.user_loader
def user_loader(id):
    return User.query.get(int(id))


app.register_blueprint(main, url_prefix='/')
app.register_blueprint(user, url_prefix='/user')