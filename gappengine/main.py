from functools import wraps
from flask import Flask, request, current_app, jsonify
import json
from flask_jsonpify import jsonify
from flask_cors import cross_origin

from flip_nlp import *

app = Flask(__name__)

@app.route('/')
@cross_origin(send_wildcard=True)
def hello():
	print("hello: request received")
	return jsonify({'results': {'success': 1, 'message': 'Welcome to Flip' } })

@app.route('/curated', methods=['GET', 'POST'])
@cross_origin(send_wildcard=True)
def curated():
	print("curated: request received")
	data = request.get_json()
	url = data["url"]
	triggers = data["triggers"]

	results = yhmh_nlp(url, triggers)
	if results is "":
		return jsonify({'results': {'success': 0, 'message': 'no recommendation' } })

	print(results)
	return jsonify({'results': {'success': 1, 'message': results } })

if __name__ == '__main__':
	app.run(host='127.0.0.1', port=8080, debug=True)
