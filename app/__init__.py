#----------------------------------------
# initialization
#----------------------------------------
from os import environ
from flask import Flask
app = Flask(__name__)
# heroku = Heroku(app)  # Sets CONFIG automagically
app.debug = True

# Set environment variables
def set_env(key):
	if key in environ:
		app.config[key] = environ[key]

set_env(key = 'TWILIO_ACCOUNT_SID')
set_env(key = 'TWILIO_AUTH_TOKEN')
set_env(key = 'TWILIO_NUMBER')
set_env(key = 'X_Parse_REST_API_Key')
set_env(key = 'X_Parse_Application_Id')