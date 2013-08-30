from flask import Flask, render_template, url_for
from flask.ext.heroku import Heroku
import requests

#----------------------------------------
# initialization
#----------------------------------------

app = Flask(__name__)
heroku = Heroku(app)  # Sets CONFIG automagically

app.config.update(
    X_Parse_Application_Id = environ.get('X-Parse-Application-Id'),
    X_Parse_REST_API_Key = environ.get('X-Parse-REST-API-Key')
)

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

if __name__ == '__main__':
    app.run(debug=True)