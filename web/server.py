import sys
sys.path.append('../')
from flask import Flask, jsonify, Request
from emptySpace.emptyspace import Empty_Space
import json

app = Flask(__name__)

@app.route('/es/v1/find_es', methods=['POST'])
def gen_empty_space():
    if Request.is_json:
        jsondata = Request.json
        print(jsondata)
        data = json.loads(jsondata)
        es = Empty_Space(data['data'], data['clusters'], 2)
        es.find_empty_space()
        scaled_data, scaled_centers = es.scale()
        toReturn = {'scaled_data':scaled_data, 'scaled_centers':scaled_centers}
        return jsonify(toReturn)

@app.route("/")
def home():
    return "nice"

