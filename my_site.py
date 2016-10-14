from flask import Flask, request, render_template, redirect, url_for,\
    flash, session, jsonify
from flask_wtf import Form
from flask_bcrypt import Bcrypt
from wtforms import StringField, PasswordField
from wtforms.validators import DataRequired
from functools import wraps
import hue
import os
from config import *
from datetime import datetime

app = Flask(__name__)
bcrypt = Bcrypt(app)
app.config.from_object(os.environ['APP_SETTINGS'])


def login_required(f):
    @wraps(f)
    def wrap(*args, **kwargs):
        if 'logged_in' in session:
            return f(*args, **kwargs)
        else:
            flash('Login required')
            return redirect(url_for('login'))
    return wrap


@app.route('/check-all-lights')
@login_required
def check_lights():
    return jsonify(hue.get_all_lights())


@app.route('/set-lights', methods=['PUT'])
@login_required
def set_lights():
    data = request.get_json(force=True)
    return jsonify(hue.turn_lights_on_off(data))


@app.route('/')
def main():
    return redirect(url_for('start_page', name='randall'))


@app.route('/home')
@login_required
def home():
    timestamp = datetime.now().strftime('%d%H%M%S')
    return render_template('index.html', timestamp=timestamp)


@app.route('/login', methods=['GET', 'POST'])
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
#                flash('Successfully logged in.')
                return redirect(url_for('home'))
            else:
                error = 'Invalid credentials'
    return render_template('login.html', form=form, error=error)


@app.route('/logout')
@login_required
def logout():
    session.pop('logged_in', None)
    flash('Logged out')
    return redirect(url_for('home'))


@app.route('/<name>')
def start_page(name):
    return render_template(name+'.html')


@app.route('/camera')
@login_required
def camera():
    timestamp = datetime.now().strftime('%d%H%M%S')
    return render_template('camera.html', timestamp=timestamp)


class LoginForm(Form):

    username = StringField(
        'username',
        validators=[DataRequired()]
    )
    password = PasswordField(
        'password',
        validators=[DataRequired()]
    )


if __name__ == '__main__':
    app.run()
