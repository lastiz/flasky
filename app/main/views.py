from datetime import datetime
from flask import (
    render_template,
    session,
    redirect,
    url_for,
    flash,
)
from . import main
from .forms import NameForm
from .. import db
from ..models import User


@main.route('/')
def index():
    return render_template('index.html', current_time=datetime.utcnow()), 200


@main.route('/user', methods=['GET', 'POST'])
def user():
    form = NameForm()
    if form.validate_on_submit():
        old_name = session.get('name')
        if old_name and old_name != form.name.data:
            flash('Looks like you\'ve changed your name!')
        session['name'] = form.name.data
        return redirect(url_for('.user'))
    return render_template('user.html', form=form, name=session.get('name')), 200
