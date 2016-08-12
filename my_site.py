from flask import Flask, request, render_template, redirect, url_for,\
flash, session, send_file
from flask_wtf import Form
from wtforms import StringField, PasswordField
from wtforms.validators import DataRequired
from functools import wraps
import hue
import os
from config import PASSWORD


app = Flask(__name__)
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


@app.route('/lights/<on_off>')
@login_required
def lights_off(on_off):
    lights = hue.get_all_lights()
    if on_off=='on':
        hue.set_all_lights_state(lights, True, hue.nice_yellow)
        flash("Lights turned on.")
    elif on_off=='off':
        hue.set_all_lights_state(lights, False, hue.nice_yellow)
        flash("Lights turned off.")
    return render_template('index.html')


@app.route('/')
def home():
    return render_template('index.html')


@app.route('/login', methods=['GET', 'POST'])
def login():
    error = None
    form = LoginForm(request.form)
    if request.method == 'POST':
        if form.validate_on_submit():
            if request.form['username'] == 'randall'\
                and request.form['password'] == PASSWORD:
                session['logged_in'] = True
                flash('Successfully logged in.')
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
    return render_template('camera.html')


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
