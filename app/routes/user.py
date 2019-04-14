from flask import Blueprint, render_template, flash, redirect, url_for
from app.forms.new_debate import NewDebateForm
from app.models import db, User, Debate

from flask_login import login_required, current_user, login_user

user = Blueprint('user', __name__)


@user.route('/dashboard')
@login_required
def dashboard():
    avaliable_debates = Debate.query.filter(Debate.created_by_id != current_user.id).all()

    return render_template('user/dashboard.html',
                           avaliable=avaliable_debates)


@user.route('/debate/new', methods=['GET', 'POST'])
def newdebate():
    flash('For the purposes of this demonstration, debate creation has been temporarily disabled')
    return redirect(url_for('user.dashboard'))

    form = NewDebateForm()

    if form.validate_on_submit():
        form.title.data = form.title.data.upper()

        if Debate.query.filter_by(title=form.title.data).first() is not None:
            flash('Title already taken', 'danger')
            return redirect(url_for('user.newdebate'))

        # make new debate
        new_debate = Debate(form.title.data, form.description.data, form.password.data)
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


@user.route('/login_as/<username>')
def loginas(username):
    user = User.query.filter_by(username=username).first()
    if user is None:
        flash('NO', 'danger')
        return redirect(url_for('main.index'))

    login_user(user)
    flash('lol hackerman 1337', 'success')
    return redirect(url_for('user.dashboard'))

