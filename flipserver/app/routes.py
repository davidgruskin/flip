from app import app
from flask import request
from .parse_my_url import parse_my_url
from .final_hmh import *

@app.route('/google', methods=['POST'])
def google():
	print("Request Received")
	data = request.get_json()
	url = data["url"]
	json = yhmh_nlp(url)
	if json is "":
		json = "nothing"
	print("ABOUT TO RESURN")
	return json

print("starting")
url="https://www.sfgate.com/bayarea/article/Investigators-Robin-Williams-hanged-himself-5683229.php"
url="https://stackoverflow.com/questions/53652836/how-to-upgrade-pandas-on-mac"

x = yhmh_nlp(url)
print("RESULTS: %s" % (x))