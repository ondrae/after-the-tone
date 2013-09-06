from flask import request
import requests, json, datetime
from app import app
from twilio import twiml
import random

@app.route('/get_numbers')
def get_numbers():
    numbers = []
    auth = (app.config['TWILIO_ACCOUNT_SID'], app.config['TWILIO_AUTH_TOKEN'])
    params = {
        "Status" : "completed",
        "StartTime" : str(datetime.date.today())
    }
    r = requests.get("http://api.twilio.com/2010-04-01/Accounts/"+app.config['TWILIO_ACCOUNT_SID']+"/Calls.json", params=params, auth=auth)
    r = r.json()
    for call in r["calls"]:
        if call["from_formatted"] not in numbers:
            numbers.append(call["from_formatted"])
    return json.dumps(numbers)

@app.route('/send_sms/<phone_number>/<message>')
def send_sms(phone_number, message):
	msg_dict = {}
	msg_dict['To'] = phone_number
	msg_dict['From'] = app.config['TWILIO_NUMBER']
	msg_dict['Body'] = message
	twilio_endpoint = "https://api.twilio.com/2010-04-01/Accounts/%s/SMS/Messages.json" % (app.config['TWILIO_ACCOUNT_SID'])
	r = requests.post("%s" %(twilio_endpoint), data = msg_dict, auth=(app.config['TWILIO_ACCOUNT_SID'], app.config['TWILIO_AUTH_TOKEN']))
	return json.dumps(r.json())

@app.route('/respond_to_incoming_sms', methods=['GET', 'POST'])
def respond_to_incoming_sms():

    # Get response messags
    headers = {
        "X-Parse-Application-Id" : app.config['X_PARSE_APPLICATION_ID'],
        "X-Parse-REST-API-Key" : app.config['X_PARSE_REST_API_KEY']
    }

    r = requests.get("https://api.parse.com/1/classes/DeathTexts", headers=headers)
    r = r.json()
    r = r['results']

    # Choose random message
    random_message = random.choice(r)
    random_message = random_message['text']

    # Send TwiML response
    resp = twiml.Response()
    resp.sms(random_message)
    return str(resp)

@app.route('/incoming_call', methods=['GET'])
def incoming_call():
    resp = twiml.Response()
    # Play an mp3
    sound = request.args.get("sound")
    resp.play(sound)
    resp.say("Now record your own message.")
    resp.record(maxLength="30", action="/handle_recording")
    return str(resp)
    
@app.route('/handle_recording', methods=['GET', 'POST'])
def handle_recording():
    """Play back the caller's recording."""
 
    recording_url = request.values.get("RecordingUrl", None)
 
    resp = twiml.Response()
    resp.say("That was beautiful.")
    return str(resp)

@app.route('/get_recordings', methods=['GET'])
def get_recordings():
    auth = (app.config['TWILIO_ACCOUNT_SID'], app.config['TWILIO_AUTH_TOKEN'])
    params = {
        "Status" : "completed",
        "StartTime" : str(datetime.date.today())
    }
    r = requests.get("http://api.twilio.com/2010-04-01/Accounts/"+app.config['TWILIO_ACCOUNT_SID']+"/Recordings.json", params=params, auth=auth)
    r = r.json()
    recordings = r['recordings']
    return json.dumps(recordings)