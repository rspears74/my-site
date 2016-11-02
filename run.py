from app import app
from home.hue import hue
from home.views import home_ctrl
from start.views import start
from personal.views import personal
from music.views import music

app.register_blueprint(hue.blueprint)
app.register_blueprint(home_ctrl)
app.register_blueprint(start)
app.register_blueprint(personal)
app.register_blueprint(music)

if __name__ == '__main__':
    app.run()
