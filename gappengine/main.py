from flask import Flask, jsonify, request

# pip install -U flask-cors
from flask_cors import cross_origin

app = Flask(__name__)

@app.route('/')
@cross_origin(send_wildcard=True)
def hello():
	return jsonify({'message': 'This is just a test!'})

@app.route('/curated', methods=['POST'])
@cross_origin(send_wildcard=True)
def curated():
	print("curated: request received")
	data = request.get_json()
	print(data)
	return "%s({'a':1, 'b':2 })" % _GET_PARAMS('callback')
	#return jsonify({'message': 'success returned!'})

@app.route('/_getData', methods=['GET', 'POST'])
@cross_origin(send_wildcard=True)
def getData():
    #hit the data, package it, put it into json.
    #ajax would have to hit this every so often to get latest data.
    arr = {}
    arr["blah"] = []
    arr["blah"].append("stuff");

    return jsonify(response=arr)

if __name__ == '__main__':
    app.run(host='127.0.0.1', port=8080, debug=True)
