import csv,requests

def main():
    url = "https://www.buddy311.org:31102"

    # get list of pending complaints
    r = requests.get(url + "/v1/pending")
    pendingComplaintsList = r.json().get("pending_complaints", [])
    if not len(pendingComplaintsList):
        print("No pending complaints found")
        return
    print("Received list of pending complaints:"+ str(pendingComplaintsList))
    pendingComplaintsList = [complaint[0] for complaint in pendingComplaintsList]

    # use the /v1/classify endpoint to classify it
    r = requests.post(url +"/v1/classify", data = {"descriptions":pendingComplaintsList})
    responseDict = r.json()
    classificationsList = responseDict.get("service_code",[])
    if not len(classificationsList):
        print("Got no classifications back")
        return
    print("Received list of classifications:"+ str(classificationsList))

    # merge the two lists together
    results = zip(pendingComplaintsList,classificationsList)
    print("Merged the results:" + str(results))

    # save results in complete.csv, appending
    requests.post(url + "/v1/complete", data = {"complete":results})
    print("Saved results in complete file.")

    # clear pending.csv
    requests.delete(url + "/v1/pending")
    print("Cleared pending file")

main()
