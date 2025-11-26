import time
from collections import defaultdict

locks = {}
wait_for = defaultdict(list)

n = int(input("Enter number of transactions: "))
m = int(input("Enter number of resources: "))

transactions = [f"T{i+1}" for i in range(n)]
resources = [f"R{i+1}" for i in range(m)]

for r in resources:
    locks[r] = None


def acquire_lock(transaction, resource):
    owner = locks[resource]
    if owner is None:
        locks[resource] = transaction
        print(f"{transaction} acquired {resource}")
    else:
        print(f"{transaction} waiting for {resource} (held by {owner})")
        wait_for[transaction].append(owner)
    time.sleep(1)


def detect_cycle():
    if len(wait_for) < 2:
        return False

    visited = set()
    rec_stack = set()

    def dfs(t):
        visited.add(t)
        rec_stack.add(t)
        for neigh in wait_for[t]:
            if neigh == t:
                continue
            if neigh not in visited:
                if dfs(neigh):
                    return True
            elif neigh in rec_stack:
                return True
        rec_stack.remove(t)
        return False

    for t in wait_for:
        if t not in visited:
            if dfs(t):
                return True
    return False


def recover_deadlock(victim):
    print(f"Deadlock detected. Aborting {victim}")
    time.sleep(1)
    for r, owner in locks.items():
        if owner == victim:
            locks[r] = None
            print(f"Released lock on {r} from {victim}")
            time.sleep(1)
    wait_for.pop(victim, None)
    for t in list(wait_for.keys()):
        if victim in wait_for[t]:
            wait_for[t].remove(victim)
    print("Deadlock resolved")
    time.sleep(1)


print("\nStarting Deadlock Simulation\n")
time.sleep(1)

if n < 2 or m < 2:
    print("Deadlock cannot occur with fewer than 2 transactions and 2 resources.")
    print("Simulation ended.")
    exit()

print("Initial Locking")
time.sleep(1)

limit = min(n, m)
for i in range(limit):
    acquire_lock(transactions[i], resources[i])

time.sleep(1)
print("\nCreating circular wait\n")
time.sleep(1)

for i in range(limit):
    acquire_lock(transactions[i], resources[(i + 1) % limit])

time.sleep(1)
print("\nWait-for Graph:")
print(dict(wait_for))
time.sleep(1)

if detect_cycle():
    recover_deadlock(transactions[-1])

print("\nRetrying locks\n")
time.sleep(1)

for i in range(limit):
    acquire_lock(transactions[i], resources[(i + 1) % limit])

print("\nFinal Locks State:", locks)
