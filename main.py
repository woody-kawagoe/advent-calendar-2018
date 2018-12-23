# coding: UTF-8
from flask import Flask
from flask import jsonify
from flask import render_template

import numpy as np
import pandas as pd
from bs4 import BeautifulSoup as bs
import json
import requests
import models

app = Flask(__name__)


@app.route('/')
def index():
    results = models.EventModel.get_dict()
    return jsonify(results)


@app.route('/task')
def task():
    events = _get_events()
    models.EventModel.put(events)
    return jsonify()


@app.route('/check')
def check():
    results = models.EventModel.get_dict()
    df = pd.DataFrame(results)
    grouped_df = df.groupby('location', as_index=False).count()
    results = [{'location': x[1][0], 'count': x[1][1]} for x in grouped_df.iterrows()]
    return jsonify(results)


@app.route('/random')
def random():
    events = list(models.EventModel.get())
    count = len(events)
    event = events[np.random.randint(count)]
    event_dict = models._entity_to_dict(event)
    file_path = 'random.html'
    return render_template(file_path, data=event_dict)


def _get_events():
    path = 'https://party-calendar.net/area/tokyo/machicon'
    r = requests.get(path)
    soup = bs(r.content, "html.parser")
    events = soup.find_all('li', 'party-event')
    events = [json.loads(x.script.text) for x in events]
    return events


if __name__ == '__main__':
    app.run(host='127.0.0.1', port=8080, debug=True)
