#----------------------------------------
# initialization
#----------------------------------------
from os import environ
from flask import Flask
app = Flask(__name__)
app.debug = True

# app.config.from_envvar('APP_SETTINGS')

# Set environment variables
def set_env(key):
	if key in environ:
		app.config[key] = environ[key]

set_env(key = 'TWILIO_ACCOUNT_SID')
set_env(key = 'TWILIO_AUTH_TOKEN')
set_env(key = 'TWILIO_NUMBER')
set_env(key = 'X_PARSE_REST_API_KEY')
set_env(key = 'X_PARSE_APPLICATION_ID')