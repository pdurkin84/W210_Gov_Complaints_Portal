from flask import Flask, request
from flask_restful import Resource, Api
import random

app = Flask(__name__)
api = Api(app)


# Superstructure for testing.  Contains all the current complaint types and the subcomplaints associated
# with them
complaints = { 
	'Street':['street_general', 'street_repair', 'street_cleaning', 'street_slippery',
   		'street_roadkill', 'street_drainage', 'street_sewer', 'street_dumping', 'street_lighting',
	'street_parking', 'street_urgent_repair', 'street_sidewalk'], 
	'vandalism': ['vandalism_general', 'vandalism_graffiti', 'vandalism_missing_signage'],
	'Environment': ['environment_general', 'environment_litter', 'environment_dumping', 'environment_abandoned_vehicle',
	    'environment_hazardous_material', 'environment_dead_animal', 'environment_overgrowth', 'environment_air_pollution', 
		'environment_water_pollution', 'environment_abandoned_site', 'environment_asbestos', 'environment_garbage_collection', 
		'environment_recycling'],
	'Planning': ['planning_general', 'planning_construction', 'planning_unsafe_environment'], 
	'Fire': ['fire_general', 'fire_illegal', 'fire', 'fire_risks', 'fire_code_violation', 'fire_equipment_broken', 
		'fire_equipment_missing', 'fire_issue_public_building'],
	'Public_Health': ['publichealth_general', 'publichealth_restaurant_hygiene', 'publichealth_school_hygiene', 
		'publichealth_public_building_hygiene', 'publichealth_public_park_hygiene', 'publichealth_animal', 
		'publichealth_animal_feces', 'publichealth_pests'],
	'Public_Order': [ 'publicorder_general', 'publicorder_jay_walking', 'publicorder_dangerous_driving', 
		'publicorder_dangerous_behavior', 'publicorder_loitering', 'publicorder_suspicious_behavior', 
		'publicorder_drug_activity', 'publicorder_noise_pollution', 'publicorder_noise_complaint'],
	'Public_Transit':['publictransit_general', 'publictransit_bus_service', 'publictransit_bus_infrastructure',
	    'publictransit_bus_costomer_relations', 'publictransit_metro_service', 'publictransit_metro_infrastructure', 
		'publictransit_metro_costomer_relations', 'publictransit_train_service', 'publictransit_train_infrastructure', 
		'publictransit_train_customer_relations'], 
	'Housing': ['housing_general', 'housing_mold', 'housing_pests', 'housing_safety', 'housing_flooding', 
		'housing_heating_cooling', 'housing_health_code', 'housing_dispute', 'housing_discrimination'],
	'Infrastructure': ['infrastructure_general', 'infrastructure_water', 'infrastructure_power'], 
	'Governance': ['governance_general', 'governance_signage', 'governance_corruption', 'governance_parks_and_rec', 
		'governance_community']
	}


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
	a field called 'textdescription' and returns the classification of the text
"""

class buddy311(Resource):

	# The POST method which receives POST http requests (data sent in JSON format)
	# and returns the classification
	def post(self):
		some_json = request.get_json()
		if some_json.get('textdescription') == None:
			return {'result': 'unknown'}
		newTextDescription = some_json.get('textdescription')
		print("received: ", newTextDescription)
		keyname = random.choice(list(complaints))
		subkeyname = complaints[keyname][random.randrange(0,len(complaints[keyname]))]
		return {'complaintType': keyname, 'complaintSubtype': subkeyname}

# Map URL paths to classes that implement the http requests for these paths
api.add_resource(test, '/')
api.add_resource(buddy311, '/buddy311/v0.1/')

# Enable debugging and set the port to 31101
if __name__ == '__main__':
	app.run(debug=True, port=31101)
