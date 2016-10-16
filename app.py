from flask import Flask
import os
from config import *

app = Flask(__name__)
app.config.from_object(os.environ['APP_SETTINGS'])
