from flask import Blueprint, render_template, flash, redirect, url_for
from app.forms.sign_up import SignUpForm
from app.forms.log_in import LogInForm
from app.models import db, User

from flask_login import login_user, logout_user, login_required

main = Blueprint('main', __name__)


@main.route('/')
@main.route('/index')
def index():
    return render_template('main/index.html')


@main.route('/signup', methods=['GET', 'POST'])
def signup():
    form = SignUpForm()

    if form.validate_on_submit():
        # check if username is valid
        user = User.query.filter_by(username=form.username.data).all()

        if user:
            flash('Username taken', 'danger')
            return redirect(url_for('main.signup'))

        flash('Cool form dude', 'success')
        new_user = User(form.username.data, form.password.data)
        db.session.add(new_user)
        db.session.commit()

    return render_template('main/signup.html',
                           sign_up_form=form)


@main.route('/login', methods=['GET', 'POST'])
def login():
    form = LogInForm()

    if form.validate_on_submit():
        user = User.query.filter_by(username=form.username.data).first()
        if user is None or not user.validate_password(form.password.data):
            flash('Incorrect Username or Password', 'danger')
            return redirect(url_for('main.login'))

        flash('Logged In successfully', 'success')
        login_user(user)
        return redirect(url_for('user.dashboard'))

    return render_template('main/login.html',
                           log_in_form=form)


@login_required
@main.route('/logout')
def logout():
    logout_user()
    flash('Logged out successfully', 'success')
    return redirect(url_for('main.index'))
