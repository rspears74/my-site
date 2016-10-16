from flask import Blueprint, jsonify, request, redirect, url_for,\
render_template, session, flash
from functools import wraps
from flask_wtf import Form
from wtforms import StringField, PasswordField
from wtforms.validators import DataRequired
from datetime import datetime
from extensions import login_required, bcrypt
from config import *

home_ctrl = Blueprint('home_ctrl', __name__, template_folder='templates')


class LoginForm(Form):
    username = StringField(
        'username',
        validators=[DataRequired()]
    )
    password = PasswordField(
        'password',
        validators=[DataRequired()]
    )


@home_ctrl.route('/logout')
@login_required
def logout():
    session.pop('logged_in', None)
    flash('Logged out')
    return redirect(url_for('home_ctrl.home'))


@home_ctrl.route('/login', methods=['GET', 'POST'])
def login():
    error = None
    form = LoginForm(request.form)
    if request.method == 'POST':
        if form.validate_on_submit():
            if request.form['username'] == 'randall'\
                and bcrypt.check_password_hash(
                    PASSWORD,
                    request.form['password']
                    ):
                session['logged_in'] = True
                return redirect(url_for('home_ctrl.home'))
            else:
                error = 'Invalid credentials'
    return render_template('login.html', form=form, error=error)



@home_ctrl.route('/home')
@login_required
def home():
    timestamp = datetime.now().strftime('%d%H%M%S')
    return render_template('home.html', timestamp=timestamp)


@home_ctrl.route('/camera')
@login_required
def camera():
    timestamp = datetime.now().strftime('%d%H%M%S')
    return render_template('camera.html', timestamp=timestamp)
