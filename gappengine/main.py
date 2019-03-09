from flask import Flask
from flask_cors import CORS, cross_origin

app = Flask(__name__)
CORS(app)

@app.route('/')
def hello():
    return 'This is just a test!'

@app.route('/curated', methods=['POST'])
def curated():
	print("curated: request received")
	data = request.get_json()
	print(data)
	return "success returned"

if __name__ == '__main__':
    app.run(host='127.0.0.1', port=8080, debug=True)
