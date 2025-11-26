# Distributed Deadlock Detection — Wait-for Graph Simulation  
**Group 08 — Distributed Systems**

---

## Overview
This project simulates **distributed deadlock detection** using a **Coordinator–Transaction model**.  
Multiple transactions request locks on shared resources, and the coordinator detects **cycles** in the  
Wait-for Graph (WFG). When a deadlock occurs, the coordinator resolves it by **aborting one transaction**  
and releasing its locks.

This simulation demonstrates how distributed systems detect and recover from deadlocks using  
central coordination.

---

# Architecture

This project follows a **Coordinator–Transaction architecture** inspired by real distributed databases:

1. **Transactions (T1 & T2)** run independently in separate VS Code terminals and request locks by  
   writing their lock requests into a shared file (`requests.json`).

2. The **Coordinator** continuously reads these incoming requests, updates the:  
   - **Lock Table** (resource → transaction holding it)  
   - **Wait-for Graph (WFG)** (transaction → transaction being waited upon)

3. A **cycle** in the WFG indicates a **deadlock**.

4. The coordinator performs **deadlock recovery** by selecting a victim transaction to abort,  
   releasing its locks, and allowing the remaining transaction to complete.

5. When all transactions finish or abort, the coordinator prints the **final lock state** and exits.

This architecture models how real systems coordinate distributed concurrency and deadlock resolution.

---

# Dependencies

This project uses only Python’s built-in libraries:

| Library | Purpose |
|--------|---------|
| `json` | Communication between coordinator and transactions |
| `time` | Simulated execution delays |
| `collections` | Wait-for Graph implementation (`defaultdict`) |
| `os` | Ensuring clean startup state |

No external installations required.

---

# How to Run the Entire Simulation (VS Code Task Runner)

To simulate a distributed environment, all three programs must run **in parallel**.  
VS Code Tasks will automatically open all required terminals.

Follow these exact steps:

**Open the project folder in VS Code**

Group_08_WaitForGraph

**Press the command palette shortcut**

Ctrl + Shift + P

**Type and select:**

Run Task

**Choose the task:**

Run All (Coordinator + T1 + T2)


This automatically launches:
- **Terminal 1 → Coordinator**  
- **Terminal 2 → Transaction T1**  
- **Terminal 3 → Transaction T2**

All three begin executing simultaneously.

**When prompted:**

“Select a problem matcher for this task”

**Choose:**

Continue without scanning the task output


---

# Expected Execution Flow

Once the tasks start:

1. **T1 acquires R1**  
2. **T2 acquires R2**  
3. T1 requests R2 → waits  
4. T2 requests R1 → waits  
5. The coordinator detects a **cycle** in the Wait-for Graph  
6. Coordinator **aborts T2** and releases R2  
7. T1 completes its work and sends DONE  
8. Coordinator prints the **final lock state** and exits

This produces a clean, deterministic demonstration of deadlock detection and recovery.

