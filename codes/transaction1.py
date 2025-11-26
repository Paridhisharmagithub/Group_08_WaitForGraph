import json, time, os
REQUEST_FILE = "requests.json"
STATUS_FILE = "statuses.json"

def append(req):
    try:
        with open(REQUEST_FILE,"r") as f:
            data = json.load(f)
    except:
        data = {"requests":[]}
    data["requests"].append(req)
    with open(REQUEST_FILE,"w") as f:
        json.dump(data,f,indent=2)

def read_status():
    try:
        with open(STATUS_FILE,"r") as f:
            return json.load(f).get("statuses",{})
    except:
        return {}

print("\nStarting Transaction T1\n")
time.sleep(0.5)

print("T1: requesting R1")
append(["T1","R1"])
time.sleep(1.2)   # allow T2 to acquire R2

print("T1: requesting R2")
append(["T1","R2"])

# do some work if not aborted; otherwise exit
start = time.time()
while True:
    st = read_status().get("T1")
    if st == "aborted":
        print("T1: detected ABORT. exiting.")
        break
    if time.time() - start > 3.0:
        print("T1: finished work; sending DONE")
        append(["T1","","done"])
        break
    time.sleep(0.5)
