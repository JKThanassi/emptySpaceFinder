from flask import Flask, jsonify, Request
from emptySpace.emptyspace import Empty_Space

app = Flask(__name__)

@app.route('es/v1/find_es', methods=['GET'])
def gen_empty_space():
    if Request.is_json:
        pass

