import requests, json, datetime
from app import app

@app.route('/get_calls')
def get_calls():
    numbers = []
    auth = (app.config['TWILIO_ACCOUNT_SID'], app.config['TWILIO_AUTH_TOKEN'])
    params = {
        "Status" : "completed",
        "StartTime" : str(datetime.date.today())
    }
    r = requests.get("http://api.twilio.com/2010-04-01/Accounts/"+app.config['TWILIO_ACCOUNT_SID']+"/Calls.json", params=params, auth=auth)
    r = r.json()
    for call in r["calls"]:
        number = {
            "number" : call["from_formatted"]
        }
        numbers.append(number)
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

