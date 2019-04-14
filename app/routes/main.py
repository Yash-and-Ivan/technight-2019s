import gevent.monkey
gevent.monkey.patch_all()

from flask import Blueprint, render_template, flash, redirect, url_for
from app.forms.sign_up import SignUpForm
from app.forms.log_in import LogInForm
from app.models import db, User

from flask_login import login_user, logout_user, login_required, current_user
from functools import wraps

from config import AZURE_KEY

main = Blueprint('main', __name__)


def anonymous_required(f):

    @wraps(f)
    def actual_decorator(*args, **kwargs):
        if current_user.is_anonymous:
            return f(*args, **kwargs)

        flash('Please log out to view this page')
        return redirect(url_for('user.dashboard'))

    return actual_decorator

@main.route('/')
@main.route('/index')
@anonymous_required
def index():
    return render_template('main/index.html')


@main.route('/signup', methods=['GET', 'POST'])
@anonymous_required
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
@anonymous_required
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


@main.route('/checkgood/<text>')
def positive_message(text):
    text_analytics_base_url = "https://eastus2.api.cognitive.microsoft.com/text/analytics/v2.0/"
    sentiment_api_url = text_analytics_base_url + "sentiment"

    docs = {'documents': [{'id': 1, 'language': 'en', 'text': text}]}
    headers = {"Ocp-Apim-Subscription-Key": AZURE_KEY}
    import requests
    response = requests.post(sentiment_api_url, headers=headers, json=docs)
    sentiment = response.json()['documents'][0]['score']
    return str(sentiment > 0.25)
