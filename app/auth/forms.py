from wtforms import (
    StringField,
    PasswordField,
    BooleanField,
    SubmitField,
    ValidationError,
)
from wtforms.validators import DataRequired, Email, Length, Regexp, EqualTo
from flask_wtf import FlaskForm
from app.models import User
from flask_login import current_user
from werkzeug.security import generate_password_hash


class LoginForm(FlaskForm):
    email = StringField('Email', validators=[DataRequired(), Length(4, 64),Email()])
    password = PasswordField('Password', validators=[DataRequired()])
    remember_me = BooleanField('Keep me logged in')
    submit_field = SubmitField('Log In')


class RegistrationForm(FlaskForm):
    email = StringField('Email', validators=[DataRequired(), Length(4, 64), Email()])
    username = StringField('Username', validators=[DataRequired(), Length(3, 64),
                                                   Regexp(r'^[A-Za-z][a-zA-Z0-9_.]*$',
                                                          0, 'Usernames must have only letters, numbers, dots or'
                                                             'underscores')])
    password = PasswordField('Password', validators=[DataRequired(),
                                                     EqualTo('password2', message='password must match')])
    password2 = PasswordField('Confirm Password', validators=[DataRequired()])
    submit = SubmitField('Register')
    
    def validate_email(self, field):
        if User.query.filter_by(email=field.data).count():
            raise ValidationError('Email already registered')
    
    def validate_username(self, field):
        if User.query.filter_by(username=field.data).count():
            raise ValidationError('Username already in use')


class ChangePasswordForm(FlaskForm):
    old_password = PasswordField('Old password', validators=[DataRequired(), Length(4, 64)])
    new_password = PasswordField('New password', validators=[DataRequired(), EqualTo('new_password2', message='password must much')])
    new_password2 = PasswordField('Confirm new password', validators=[DataRequired()])
    submit = SubmitField('Change')
    
    def validate_old_password(self, field):
        user = User.query.get(current_user.get_id())
        if not user.verify_password(field.data):
            raise ValidationError('Old password isn\'t correct')
    
    def validate_new_password(self, field):
        user = User.query.get(current_user.get_id())
        if user.password_hash == generate_password_hash(field.data):
            ValidationError('New password must be different from old one')