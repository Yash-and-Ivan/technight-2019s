from flask import Blueprint, render_template, flash, redirect, url_for
from app.forms.sign_up import SignUpForm
from app.forms.log_in import LogInForm
from app.models import db, User, Debate

from flask_login import login_user, logout_user, login_required, current_user
from functools import wraps

debate = Blueprint('debate', __name__)

import sys


# valid url blueprint
def spectator_required(f):
    @wraps(f)
    def actual_decorator(*args, **kwargs):
        debate = Debate.query.filter_by(url=kwargs['url']).first()

        if debate is None or debate.created_by.id == current_user.id:
            flash('You are not allowed to spectate this debate')
            return redirect(url_for('user.dashboard'))

        return f(*args, **kwargs)
    return actual_decorator


@debate.route('/<url>/spectate')
@login_required
@spectator_required
def spectate(url):
    debate = Debate.query.filter_by(url=url).first()
    assert(debate is not None)

    return render_template('debate/spectate.html',
                           navbar_extra=' - ' + debate.title)
