from flask import Blueprint, render_template


eng = Blueprint('eng', __name__, template_folder='templates')


@eng.route('/eng')
def home():
    return render_template('enghome.html')


@eng.route('/mvbridge')
def mvbridgepage():
    return render_template('mvbridge.html')


@eng.route('/mvplots')
def mvplotpage():
    return render_template('mvplot.html')


@eng.route('/vreact')
def vreactpage():
    return render_template('vreact.html')


@eng.route('/beam')
def beampage():
    return render_template('beam.html')


@eng.route('/test')
def testplot():
    return render_template('plotlytest.html')
