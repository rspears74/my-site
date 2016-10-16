from flask import Blueprint, render_template

start = Blueprint('start', __name__, template_folder='templates')

@start.route('/<name>')
def start_page(name):
    return render_template(name+'.html')
