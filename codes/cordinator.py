import json
import time
from collections import defaultdict
import os

REQUEST_FILE = "requests.json"
STATUS_FILE = "statuses.json"
SLEEP = 0.8

locks = {}
wait_for = defaultdict(list)
txn_status = {}

def init_files():
    # start clean for demo
    with open(REQUEST_FILE, "w") as f:
        json.dump({"requests": []}, f)
    with open(STATUS_FILE, "w") as f:
        json.dump({"statuses": {}}, f)

def load_requests():
    try:
        with open(REQUEST_FILE, "r") as f:
            return json.load(f).get("requests", [])
    except:
        return []

def save_requests(reqs):
    with open(REQUEST_FILE, "w") as f:
        json.dump({"requests": reqs}, f, indent=2)

def save_statuses():
    with open(STATUS_FILE, "w") as f:
        json.dump({"statuses": txn_status}, f, indent=2)

def print_header(text):
    print("\n" + text + "\n")

def process(entry):
    # entry: ["T1","R1"] or ["T1","","done"]
    if not isinstance(entry, list) or len(entry) < 2:
        return
    txn = entry[0]
    res = entry[1]
    action = entry[2] if len(entry) > 2 else "acquire"

    if txn_status.get(txn) in ("aborted", "done"):
        return

    txn_status.setdefault(txn, "active")

    if action in ("done", "commit"):
        for r, o in list(locks.items()):
            if o == txn:
                locks[r] = None
                print(f"{txn} released {r}")
        txn_status[txn] = "done"
        return

    if res not in locks:
        locks[res] = None

    owner = locks[res]
    if owner is None:
        locks[res] = txn
        print(f"{txn} acquired {res}")
    else:
        if owner == txn:
            return
        if owner not in wait_for[txn]:
            wait_for[txn].append(owner)
        print(f"{txn} waiting for {res} (held by {owner})")

def detect_pair_cycle():
    # simple pairwise check (works for demo)
    for a in wait_for:
        for b in wait_for[a]:
            if a in wait_for.get(b, []):
                return True, (a, b)
    return False, None

def print_state():
    print_header("==================  COORDINATOR SNAPSHOT  ==================")
    act = [t for t,s in txn_status.items() if s=="active"]
    print(" Active Transactions:", ", ".join(act) if act else "None")
    print("\n Current Locks:")
    if not locks:
        print("  No locks yet.")
    else:
        for r,o in locks.items():
            print(f"  {r} -> {'free' if o is None else o}")
    print("\n Wait-For Graph:")
    if any(wait_for.values()):
        for t in wait_for:
            if wait_for[t]:
                print(f"  {t} waits for {', '.join(wait_for[t])}")
    else:
        print("  No waits.")
    print("--------------------------------------------------------")

def main():
    init_files()
    print("Coordinator started (simple demo). Waiting for requests...\n")
    time.sleep(0.6)

    while True:
        reqs = load_requests()
        if reqs:
            entry = reqs.pop(0)
            process(entry)
            save_requests(reqs)

            # detect deadlock
            dead, pair = detect_pair_cycle()
            if dead:
                a,b = pair
                # pick victim = b (as in earlier behavior)
                victim = b
                print_header(f"\nDEADLOCK detected between {a} and {b}")
                print(f"Aborting {victim} ...")
                txn_status[victim] = "aborted"
                for r,o in list(locks.items()):
                    if o == victim:
                        locks[r] = None
                        print(f"Coordinator released {r} from {victim}")
                # remove victim from wait_for
                wait_for.pop(victim, None)
                for t in list(wait_for.keys()):
                    if victim in wait_for[t]:
                        wait_for[t].remove(victim)
                save_statuses()
                # continue to let other txn finish
        # show simple state periodically
        print_state()
        # termination: when at least one txn existed and now none active and no pending requests
        any_active = any(s=="active" for s in txn_status.values())
        pending = len(load_requests())>0
        if not any_active and not pending and txn_status:
            print("\nFinal Locks State:", locks)
            print("\nCoordinator exiting.")
            break
        time.sleep(SLEEP)

if __name__ == "__main__":
    main()
