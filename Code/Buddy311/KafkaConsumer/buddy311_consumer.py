import json
from kafka import KafkaConsumer
import mysql.connector as mariadb
import requests

# Create the database connection
mariadb_connection = mariadb.connect(host='database', user='buddy311dba', password='AlexChrisPaulStan', database='buddy311')
cursor = mariadb_connection.cursor()

consumer = KafkaConsumer('buddy311', bootstrap_servers=['kafkaserver1:9092'], value_deserializer=lambda m: json.loads(m.decode('utf-8')))

for message in consumer:
    # message value and key are raw bytes -- decode if necessary!
	# e.g., for unicode: `message.value.decode('utf-8')`
	print ("Message value: ", message.value)

	# send request to buddy311 REST server
	response=requests.post("http://buddy311Class:31102/buddy311/v0.1/", json=message.value)
	print("Response is: ", response.json())
	# update the database
	print("Response service_code is: ", response.json()['service_code'])
	cursor.execute("update requests set service_code=\"%s\" where service_request_id = %d" % (response.json()['service_code'], message.value['service_request_id']))
	mariadb_connection.commit()

