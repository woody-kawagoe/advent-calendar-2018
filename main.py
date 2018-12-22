# Copyright 2018 Google LLC
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

# [START gae_python37_app]
from flask import Flask
from flask import jsonify
from flask import render_template

from config import QIITA_TOKEN

import numpy as np
import requests
import models 

from google.cloud import datastore
# If `entrypoint` is not defined in app.yaml, App Engine will look for an app
# called `app` in `main.py`.
app = Flask(__name__)


@app.route('/')
def index():
    results = models.QiitaModel.get_dict()
    return jsonify(results)


@app.route('/task')
def task():
    query = 'tag:GCP'
    qiita_pages = _get_qiita_pages(query)
    models.QiitaModel.put(qiita_pages)
    return jsonify() 


@app.route('/hint')
def hint():
    pages = list(models.QiitaModel.get())
    count = len(pages)
    page = pages[np.random.randint(count)]
    page_dict = models._entity_to_dict(page)
    file_path = 'hint.html'
    return render_template(file_path, data=page_dict) 


def _get_qiita_pages(query=''):
    path = 'https://qiita.com/api/v2/items'
    if query != '':
        path = path + '?query=' + query 
    r = requests.get(path)
    return r.json() 


if __name__ == '__main__':
    # This is used when running locally only. When deploying to Google App
    # Engine, a webserver process such as Gunicorn will serve the app. This
    # can be configured by adding an `entrypoint` to app.yaml.
    app.run(host='127.0.0.1', port=8080, debug=True)
# [END gae_python37_app]
