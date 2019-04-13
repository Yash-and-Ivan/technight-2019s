from flask import Blueprint, render_template, flash, redirect, url_for
from app.forms.new_debate import NewDebateForm
from app.models import db, User, Debate

from flask_login import login_required, current_user

user = Blueprint('user', __name__)


@user.route('/dashboard')
@login_required
def dashboard():

    return render_template('user/dashboard.html')


@user.route('/debate/new', methods=['GET', 'POST'])
def newdebate():
    form = NewDebateForm()

    if form.validate_on_submit():
        form.title.data = form.title.data.upper()

        if Debate.query.filter_by(title=form.title.data).first() is not None:
            flash('Title already taken', 'danger')
            return redirect(url_for('user.newdebate'))

        # make new debate
        new_debate = Debate(form.title.data, form.description.data)
        current_user.debates.append(new_debate)
        db.session.add(new_debate)
        db.session.commit()
        flash('New Debate Created!', 'success')
        return redirect(url_for('user.dashboard'))

    return render_template('user/newdebate.html',
                           new_debate_form=form)


@user.route('/debate/<url>/delete')
@login_required
def deletedebate(url):
    debate = Debate.query.filter_by(url=url).first()

    if debate is not None and debate.created_by.id == current_user.id:
        db.session.delete(debate)
        db.session.commit()

    flash('Debate deleted', 'success')

    return redirect(url_for('user.dashboard'))
