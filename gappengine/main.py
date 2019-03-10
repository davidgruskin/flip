from functools import wraps
from flask import Flask, request, current_app, jsonify


# pip install -U flask-cors
from flask_cors import cross_origin

app = Flask(__name__)

def support_jsonp(f):
    """Wraps output to JSONP"""
    @wraps(f)
    def decorated_function(*args, **kwargs):
        result = jsonify(f(*args, **kwargs))
        callback = request.args.get('callback', False)
        if callback:
            content = str(callback) + '(' + str(result.data) + ')'
            return current_app.response_class(content,
                                              mimetype='application/json')
        else:
            return result
    return decorated_function

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
    data = request.get_json()
    for x in request.args:
    	if "mydata" in x:
    		print("MY DATA: %s" % ( x.get("mydata", "NOTHING") ))
    	print("LOST DATA: %s" % (x))
    arr = {}
    arr["blah"] = []
    arr["blah"].append("stuff");

    return jsonify(response=arr)

if __name__ == '__main__':
    app.run(host='127.0.0.1', port=8080, debug=True)
