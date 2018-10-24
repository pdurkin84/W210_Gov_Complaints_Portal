from flask import Flask, request
from flask_restful import Resource, Api
from flask_cors import CORS
import random
from finetune import Classifier
import pandas
from sklearn.model_selection import train_test_split
import time
import re, string

app = Flask(__name__)
cors = CORS(app, resources={r"*":{"origins": "*"}})
api = Api(app)
model = None

class test(Resource):
	def get(self):
		return{'result':'Server is active'}

	def post(self):
		some_json = request.get_json()
		if some_json.get('name') == None:
			print("Did not receive a name field")
		else:
			print("name received: ", some_json.get('name'))
		return {'you sent': some_json}, 201

"""
The class to implement our Buddy311 REST interface
Usage: simply implement the post method that sends in a text in JSON format in
	a field called 'description' and returns the classification of the text
"""

class buddy311(Resource):

	model = None
	# The POST method which receives POST http requests (data sent in JSON format)
	# and returns the classification
	def post(self):
		global model
		if model == None:
			model = Classifier(max_length=512, val_interval=3000, verbose = True)
			model = Classifier.load("/root/combined_model_20181021")
		some_json = request.get_json()
		if some_json.get('description') == None:
			return {'service_code': 'unknown'}
		newTextDescription = some_json.get('description')
		print("received: ", newTextDescription)
		prediction = model.predict([newTextDescription])
		return {'service_code': prediction[0]}

# Map URL paths to classes that implement the http requests for these paths
api.add_resource(test, '/')
api.add_resource(buddy311, '/buddy311/v0.1/')

# Enable debugging and set the port to 31101
if __name__ == '__main__':
	app.run(debug=True, port=31102, host='169.63.3.115', ssl_context='adhoc')
