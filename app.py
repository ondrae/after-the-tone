from flask import Flask, render_template, url_for
from flask import Response
from flask.ext.heroku import Heroku
import requests, os

#----------------------------------------
# initialization
#----------------------------------------

app = Flask(__name__)
app.config.from_pyfile('settings.cfg', silent=True)
heroku = Heroku(app)  # Sets CONFIG automagically

X_Parse_Application_Id = os.environ.get('X-Parse-Application-Id')
X_Parse_REST_API_Key = os.environ.get('X-Parse-REST-API-Key')

#----------------------------------------
# Routes
#----------------------------------------

@app.route('/')
def index():
    headers = {
        "X-Parse-Application-Id" : X_Parse_Application_Id,
        "X-Parse-REST-API-Key" : X_Parse_REST_API_Key
    }
    r = requests.get("https://api.parse.com/1/classes/DeathSwitchMessage", headers=headers)
    r = r.json()
    death_switch_message = r['results'][0]['text']
    
    r = requests.get("https://api.parse.com/1/classes/DeathTexts", headers=headers)
    r = r.json()
    r = r['results']
    death_texts = []
    for i in r:
        death_texts.append(i['text'])
    return render_template('index.html', death_switch_message=death_switch_message, death_texts=death_texts)

@app.route('/voicemail')
def voicemail():
  sound = "http://glacial-thicket-7208.herokuapp.com/static/i-have-died.mp3"
  xml = '<?xml version="1.0" encoding="UTF-8"?><Response><Play>%s</Play></Response>' % (sound)
  return Response(xml, mimetype ='text/xml')

  
if __name__ == '__main__':
    app.run(debug=True)

