from flask import Flask, render_template, url_for, request
from flask import Response
from flask.ext.heroku import Heroku
from app import app
import requests, os, json, datetime


#----------------------------------------
# Routes
#----------------------------------------

@app.route('/')
def index():
    headers = {
        "X-Parse-Application-Id" : app.config['X_PARSE_APPLICATION_ID'],
        "X-Parse-REST-API-Key" : app.config['X_PARSE_REST_API_KEY']
    }
    r = requests.get("https://api.parse.com/1/classes/DeathSwitchMessage", headers=headers)
    r = r.json()
    death_switch_messages = r['results']
    death_switch_message = death_switch_messages.pop()
    death_switch_message = death_switch_message["text"]
    
    r = requests.get("https://api.parse.com/1/classes/DeathTexts", headers=headers)
    r = r.json()
    r = r['results']
    death_texts = []
    for i in r:
        death_texts.append(i['text'])
    return render_template('index.html', death_switch_message=death_switch_message, death_texts=death_texts)

@app.route('/save_text', methods=['POST'])
def save_text():
    headers = {
        "X-Parse-Application-Id" : app.config['X_PARSE_APPLICATION_ID'],
        "X-Parse-REST-API-Key" : app.config['X_PARSE_REST_API_KEY']
    }
    id = request.form['id']
    post_data = json.dumps({"text" : request.form['value']})
    
    if id == 'death-switch-message':
        requests.post("https://api.parse.com/1/classes/DeathSwitchMessage/", data=post_data, headers=headers)
    return json.loads(post_data)["text"]

@app.route('/voicemail', methods=['GET', 'POST'])
def voicemail():
    if request.method == 'GET':
        sound = "http://after-the-tone.s3-us-west-1.amazonaws.com/i-have-died.mp3"
        xml = '<?xml version="1.0" encoding="UTF-8"?><Response><Play>%s</Play></Response>' % (sound)
        return Response(xml, mimetype ='text/xml')

    if request.method == "POST":
        pass
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
        number = call["from_formatted"]
        numbers.append(number)
    return str(numbers)

