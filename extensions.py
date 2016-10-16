from functools import wraps
from flask import session, redirect, url_for, flash
from flask_bcrypt import Bcrypt
from app import app

def login_required(f):
    @wraps(f)
    def wrap(*args, **kwargs):
        if 'logged_in' in session:
            return f(*args, **kwargs)
        else:
            flash('Login required')
            return redirect(url_for('home_ctrl.login'))
    return wrap

bcrypt = Bcrypt(app)
