import sys
sys.path.append('../')
from flask import Flask, jsonify, request
from emptySpace.emptyspace import Empty_Space
import json
import numpy as np

app = Flask(__name__)

@app.route('/es/v1/find_es', methods=['POST'])
def gen_empty_space():
    """This function handles api requests for to calculate emptyspace on the given datasets
    
    Returns:
        JSON: The data--mds scaled to 2d--embedded with empty space points and the number of empty space points returned
    """

    if request.is_json:
        jsondata = request.get_json()
        # the raw csv-formatted data
        data = json.loads(jsondata['data'])
        # the max number of clusters for k-means consider
        n_clusters = json.loads(jsondata['n_clusters'])
        es = Empty_Space(np.genfromtxt(data, delimiter=","), n_clusters, 2)
        es.find_empty_space()
        scaled_data, scaled_centers = es.scale()
        toReturn = {'scaled_data':es.toReactVisFormat(scaled_data), 'scaled_centers':es.toReactVisFormat(scaled_centers, es.ghost_point_avg_dist)}
        return jsonify(toReturn)

@app.route("/")
def home(): 
    return "This server is for the API you should not reach this page"

