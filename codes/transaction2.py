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

print("\nStarting Transaction T2\n")
time.sleep(0.5)

print("T2: requesting R2")
append(["T2","R2"])
time.sleep(1.0)

print("T2: requesting R1")
append(["T2","R1"])

# wait for possible abort; if aborted exit cleanly
while True:
    st = read_status().get("T2")
    if st == "aborted":
        print("T2: detected ABORT. exiting.")
        break
    time.sleep(0.5)
