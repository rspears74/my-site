activate_this = '/home/randall/.virtualenvs/my-site/bin/activate_this.py'
with open(activate_this) as file_:
    exec(file_.read(), dict(__file__=activate_this))

from my-site import app as application
