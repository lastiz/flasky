from flask import render_template, redirect, request, url_for, flash
from flask_login import logout_user, login_required, login_user, current_user
from . import auth
from .forms import LoginForm, ChangePasswordForm, RegistrationForm
from app.models import User
from app import db


@auth.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        if user and user.verify_password(form.password.data):
            login_user(user)
            nxt = request.args.get('next')
            if not nxt or not nxt.startswith('/'):
                nxt = url_for('main.index')
            return redirect(nxt)
        flash('Invalid email or password!', category='error')
    return render_template('auth/login.html', form=form)

@auth.route('/logout')
@login_required
def logout():
    logout_user()
    flash('You\'ve been logged out')
    return redirect(url_for('main.index'))

@auth.route('/register', methods=['GET', 'POST'])
def register():
    form = RegistrationForm()
    if form.validate_on_submit():
        user = User(
            email=form.email.data,
            username=form.username.data,
            password=form.password.data,
        )
        db.session.add(user)
        db.session.commit()
        flash('you can now login')
        return redirect(url_for('auth.login'))
    return render_template('auth/register.html', form=form)
        
@auth.route('/change_password', methods=['GET', 'POST'])
@login_required
def change_password():
    form = ChangePasswordForm()
    user = User.query.get(current_user.get_id())
    if form.validate_on_submit():
        user.password = form.new_password.data
        db.session.add(user)
        db.session.commit()
        flash('New password successfully set! You may Sign in with new password')
        return redirect(url_for('auth.login'))
    return render_template('auth/change_password.html', form=form)

@auth.before_app_request
def before_request():
    if current_user.is_authenticated:
        current_user.ping()