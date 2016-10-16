from app import app
from home.hue import hue
from home.views import home_ctrl
from start.views import start
from personal.views import personal

app.register_blueprint(hue.blueprint)
app.register_blueprint(home_ctrl)
app.register_blueprint(start)
app.register_blueprint(personal)

if __name__ == '__main__':
    app.run()
