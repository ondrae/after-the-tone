import os
from os import environ
from flask import Flask

# Initialize Flask app 
app = Flask(__name__)
app.debug = True
app.config.from_pyfile('settings.cfg', silent=True)
