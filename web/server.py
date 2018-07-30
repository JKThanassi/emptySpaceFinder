import sys
sys.path.append('../')
from flask import Flask, jsonify, request
from emptySpace.emptyspace import Empty_Space
import json
import numpy as np

app = Flask(__name__)

@app.route('/es/v1/find_es', methods=['POST'])
def gen_empty_space():
    if request.is_json:
        jsondata = request.get_json()
        data = json.loads(jsondata['data'])
        n_clusters = json.loads(jsondata['n_clusters'])
        es = Empty_Space(np.asarray(data), n_clusters, 2)
        es.find_empty_space()
        scaled_data, scaled_centers = es.scale()
        toReturn = {'scaled_data':scaled_data, 'scaled_centers':scaled_centers}
        return jsonify(toReturn)

@app.route("/")
def home():
    return "Site to come"

