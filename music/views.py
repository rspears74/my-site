from flask import Blueprint, render_template, send_file
import os
from zipfile import ZipFile, ZipInfo, ZIP_DEFLATED
from io import BytesIO
from extensions import login_required

music = Blueprint('music', __name__, template_folder='templates')

@music.route('/tunes/<path:filepath>')
@login_required
def nav(filepath):
	fullpath = '/media/randall/RANDALL/' + filepath
	fldrs = [fldr for fldr in os.listdir(fullpath) if fldr[0] != '.']
	return render_template('home.html', folders=fldrs, filepath=filepath)

@music.route('/download/<path:filepath>')
@login_required
def download(filepath):
	fullpath = '/media/randall/RANDALL/' + filepath
	mem_file = BytesIO()
	with ZipFile(mem_file, 'w') as zf:
		files = os.listdir(fullpath)
		os.chdir(fullpath)
		for f in files:
			zf.write(f)
	mem_file.seek(0)
	fname = filepath.split('/')[-1]
	return send_file(mem_file, attachment_filename=fname+".zip", as_attachment=True)
