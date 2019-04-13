from flask import Blueprint, render_template, flash, redirect, url_for
from app.forms.sign_up import SignUpForm
from app.forms.log_in import LogInForm
from app.models import db, User

from flask_login import login_user

user = Blueprint('user', __name__)


@user.route('/dashboard')
def dashboard():

    return render_template('dashboard.html')
