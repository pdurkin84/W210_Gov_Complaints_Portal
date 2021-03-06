import ssl
from sanic import Sanic
from sanic.response import json
from sanic_cors import CORS, cross_origin
import re, string, csv
import multiprocessing
import json as jsn
from finetune import Classifier
import os.path

app = Sanic()
CORS(app)

# Once we have workers each (sadly) must load its own model
#model = Classifier.load("/root/combined_model_20181021")
model=None

def loadConfiguration(file):
    with open(file) as json_data_file:
        data=jsn.load(json_data_file)

    # verify mandatory parameters and set defaults
    if data.get('modelfile') == None or not os.path.isfile(data.get('modelfile')):
        print("Unable to find model file, exiting")
        exit(1)
    if data.get('port') == None:
        data['port'] = 31102
    if data.get('hostip') == None:
        data['hostip'] = "0.0.0.0"

    print("Data is: ", data)
    return data

translator = str.maketrans('', '', string.punctuation) # To remove punctuation

def preProcess(complaintStart):
    complaint = complaintStart[:512] # cut to 512 characters max
    complaint = re.sub("\d","N", complaint) # remove numbers
    complaint = complaint.lower().translate(translator) # lower case and remove the punctuation
    complaint = complaint.replace("\n"," ").strip() # remove starting and trailing white spaces
    if re.search('[a-zA-Z]', complaint) is None:# if there are no letters in the complaint, return empty, will be removed in later processing
        return ""
    return complaint

@app.route('/v1', methods=['GET'])
async def testServerAvailability(request):
    print(request)
    return json({'result': 'Server is active'})

@app.route('/v1/complaint', methods=['POST','GET','OPTIONS'])
async def classifyOpen311Complaint(request):
    global model

    # Check if data provided
    if request.json == None:
        return json({"result", "No data in request"})

    # Check if we have a 311 'description' field
    if request.json.get('description') == None and request.json.get('descriptions') == None:
        return json({'service_code': 'unknown'})

    # If the model is not already loaded then load it
    if model == None:
        model = Classifier(max_length=512, val_interval=3000, verbose = True)
        model = Classifier.load("/root/combined_model_20181021")

    if request.json.get('descriptions') != None:
        processedComplaints = list(map(lambda x: preProcess(x), request.json.get('descriptions')))
        prediction = model.predict(processedComplaints).tolist()
    else:
        print("Doing simple prediction")
        prediction = model.predict([preProcess(request.json.get('description'))])[0]

    print("Prediction is: ", prediction)

    # If we have a service_code in the incoming request then we assume an Open311 message,
    # so we update the service_code and return the full message.  Otherwise we just send
    # back a new message with the service_code only
    if request.json.get('service_code') == None:
        print("No service code provided, returning one")
        return json({'service_code': prediction})
    else:
        print("Service_code was provided so updating it")
        request.json['service_code'] = prediction
        return json(request.json)

"""
handle calls from google assistant
"""
@app.route('/v1/assistant', methods=['POST','GET','OPTIONS'])
async def processGoogleActionRequest(request):
    print("Received POST request from google assistant")

    # Check if data provided
    if request.json == None:
        return json({'fulfillmentText': 'We did not receive a complaint, could you repeat that?'})
    some_json = request.json
    if some_json.get('queryResult') == None:
        print("Empty message text")
        return json({'fulfillmentText': 'We did not receive a complaint, could you repeat that?'})
    queryResult = some_json.get('queryResult')
    if queryResult.get('queryText') == None:
        print("Empty message text")
        return json({'fulfillmentText': 'We did not receive a complaint, could you repeat that?'})
    complaint = queryResult.get('queryText')
    print("received: ", complaint)

    with open(config.get("pendingfile"),"a", newline='') as f:
        csvWriter = csv.writer(f, delimiter = "\t")
        csvWriter.writerow([complaint])
    
    return json({'fulfillmentText': "Thank you, your complaint has been recorded and is being processed"})

"""
handle pending complaints (read, delete all)
"""
@app.route("/v1/pending", methods = ["GET", "DELETE"])
async def getPendingComplaints(request):
    if request.method == "GET":
        print("Received GET request for pending complaints")
        pendingComplaintsList = []
        try:
            with open(config.get("pendingfile"),"r") as f:
                csvReader = csv.reader(f)
                pendingComplaintsList = list(csvReader)
        except Exception as e:
            print("Error while opening pending file: "+str(e))
        return json({"pending_complaints":pendingComplaintsList})
    else:
        print("Received DELETE request for pending complaints. Clearing file")
        open(config.get("pendingfile"),"w").close()
        return json({"status":"Pending file cleared"})

"""
handle complete complaints (read, append)
"""
@app.route("/v1/complete", methods = ["GET", "POST"])
async def getCompleteComplaints(request):
    if request.method == "GET":
        print("Received GET request for complete complaints")
        completeComplaintsList = []
        try:
            with open(config.get("completefile"),"r") as f:
                csvReader = csv.reader(f)
                completeComplaintsList = list(csvReader)
        except Exception as e:
            print("Error while opening complete file: "+str(e))
        return json({"complete_complaints":completeComplaintsList})
    else:
        print("Received POST request for complete complaints. Appending new complaints")
        # Check if data provided
        if request.json == None:
            print("No complaints provided")
            return "No complaints provided"
        some_json = request.json
        if some_json.get('complete') == None:
            print("No complaints provided")
            return "No complaints provided"
        completedComplaintsList = some_json.get('complete')
        with open(config.get("completefile"),"a", newline='') as f:
            csvWriter = csv.writer(f, delimiter = "\t")
            for complaint, classification in completedComplaintsList:
                csvWriter.writerow([complaint, classification])
        return json({"status":"Complaints written to file"})

config = loadConfiguration('buddy311.json')
context = ssl.create_default_context(purpose=ssl.Purpose.CLIENT_AUTH)
if config.get('cafile') != None:
    context.load_verify_locations('/etc/ssl/certs/www_buddy311_org.ca-bundle')
context.load_cert_chain(config.get('crtfile'), keyfile=config.get('keyfile'))

cpu_cores=multiprocessing.cpu_count()
print("CPU count: " ,cpu_cores)
if __name__ == '__main__':
    #app.run(host='0.0.0.0', port=31102,ssl=context, workers=cpu_cores, debug=False)
    app.run(host=config.get('hostip'), port=int(config.get('port')),ssl=context, workers=cpu_cores, debug=False)
