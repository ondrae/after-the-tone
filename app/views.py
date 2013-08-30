from flask import Flask, render_template, url_for
from flask import Response
from flask.ext.heroku import Heroku
from app import app
import os

#----------------------------------------
# Routes
#----------------------------------------

@app.route('/')
def index():
  # url_for('show_request_for_x',
    f = open(os.path.join(app.root_path, 'static/death_switch_message.txt'), 'r')
    death_switch_message = f.read()
    f.close()
    f = open(os.path.join(app.root_path,'static/death_texts.txt'),'r')
    death_texts = f.readlines()
    f.close()
    return render_template('index.html', death_switch_message=death_switch_message, death_texts=death_texts)

@app.route('/voicemail')
def voicemail():
  sound = "http://glacial-thicket-7208.herokuapp.com/static/i-have-died.mp3"
  xml = '<?xml version="1.0" encoding="UTF-8"?><Response><Play>%s</Play></Response>' % (sound)
  return Response(xml, mimetype ='text/xml')


if __name__ == '__main__':
    app.run(debug=True)

