from flask import Blueprint, render_template

personal = Blueprint('personal', __name__, template_folder='templates')

@personal.route('/')
def homepage():
    return render_template('index.html')
