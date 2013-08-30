import requests
from app import app

def send_sms(recipient_number, message = "You are grrrreat."):
	msg_dict = {}
	msg_dict['To'] = recipient_number
	msg_dict['From'] = app.config['TWILIO_NUMBER']
	msg_dict['Body'] = message
	twilio_endpoint = "https://api.twilio.com/2010-04-01/Accounts/%s/SMS/Messages.json" % (app.config['TWILIO_ACCOUNT_SID'])
	r = requests.post("%s" %(twilio_endpoint), data = msg_dict, auth=(app.config['TWILIO_ACCOUNT_SID'], app.config['TWILIO_AUTH_TOKEN']))
	print r.json()

