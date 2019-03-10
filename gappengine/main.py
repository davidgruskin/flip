from flask import Flask

# pip install -U flask-cors
from flask_cors import cross_origin

app = Flask(__name__)

@app.route('/')
@cross_origin(send_wildcard=True)
def hello():
	self.response.headers['Access-Control-Allow-Origin'] = '*'
    return 'This is just a test!'

@app.route('/curated', methods=['POST'])
@cross_origin(send_wildcard=True)
def curated():
	self.response.headers['Access-Control-Allow-Origin'] = '*'
	print("curated: request received")
	data = request.get_json()
	print(data)
	return "success returned"

if __name__ == '__main__':
    app.run(host='127.0.0.1', port=8080, debug=True)
