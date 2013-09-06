from flask import Flask, render_template, url_for, request
from flask import Response
from app import app
import requests, os, json
import twilio_routes

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
        # sound = "http://after-the-tone.s3-us-west-1.amazonaws.com/i-have-died.mp3"
        sound = request.args.get("sound")
        xml = '<?xml version="1.0" encoding="UTF-8"?><Response><Play>%s</Play></Response>' % (sound)
        return Response(xml, mimetype ='text/xml')

    if request.method == "POST":
        pass

