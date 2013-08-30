from flask import Flask, render_template, url_for
from flask.ext.heroku import Heroku
# import requests

#----------------------------------------
# initialization
#----------------------------------------

app = Flask(__name__)
heroku = Heroku(app)  # Sets CONFIG automagically

#----------------------------------------
# Routes
#----------------------------------------

@app.route('/')
def index():
    f = open('static/death_switch_message.txt','r')
    death_switch_message = f.read()
    f.close()
    f = open('static/death_texts.txt','r')
    death_texts = f.readlines()
    f.close()
    return render_template('index.html', death_switch_message=death_switch_message, death_texts=death_texts)

if __name__ == '__main__':
    app.run(debug=True)