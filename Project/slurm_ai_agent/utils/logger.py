#!/usr/bin/env python3
import subprocess, time, json, os, datetime

STATE_FILE = "shared_state.json"
PENDING_THRESHOLD = 5  # minutes

# -----------------------------
# SAFE HELPERS
# -----------------------------
def get_timestamp_minutes(ts):
    try:
        t = datetime.datetime.strptime(ts, "%Y-%m-%dT%H:%M:%S")
        return round((datetime.datetime.now() - t).total_seconds() / 60, 1)
    except:
        return 0


def load_state():
    if not os.path.exists(STATE_FILE):
        return {}
    try:
        return json.load(open(STATE_FILE))
    except:
        return {}


def save_state(data):
    json.dump(data, open(STATE_FILE, "w"), indent=4)


# -----------------------------
# SLURM SAFE PARSER
# -----------------------------
def get_jobs():
    """
    Safely parse SLURM job lines:
    id | status | reason | nodes | submit_time
    """
    out = subprocess.getoutput("squeue -h -o '%i|%t|%R|%D|%V'")
    jobs = []

    for line in out.split("\n"):
        if "|" not in line:
            continue

        parts = line.split("|")
        if len(parts) < 5:
            print(f"[WARN] Malformed squeue line skipped: {line}")
            continue

        jid, st, reason, nodes, submit = parts[:5]

        try:
            jobs.append({
                "id": int(jid),
                "status": st.strip(),
                "reason": reason.strip(),
                "nodes": int(nodes),
                "submit": submit.strip()
            })
        except Exception as e:
            print(f"[WARN] Could not parse line: {line} | Error: {e}")
            continue

    return jobs


def get_cluster_nodes():
    try:
        total = int(subprocess.getoutput("sinfo -h -o '%n' | wc -l"))
        idle = int(subprocess.getoutput("sinfo -h -t idle -o '%n' | wc -l"))
        return total, idle
    except:
        return 0, 0


# -----------------------------
# PENDING CLASSIFIER
# -----------------------------
INVALID_KEYWORDS = [
    "invalid", "bad", "unknown", "down", "reserved", "reqnodenotavail",
    "invalidqos", "invalidconstraint", "partitiondown"
]

def classify_pending(job, total_nodes, idle_nodes):
    reason = job["reason"].lower()
    need = job["nodes"]

    for word in INVALID_KEYWORDS:
        if word in reason:
            return "PENDING_INVALID"

    if need > total_nodes:
        return "PENDING_SHORTAGE"

    if need <= total_nodes and idle_nodes < need:
        return "PENDING_QUEUE_WAIT"

    return "PENDING_OTHER"


# -----------------------------
# CORE PENDING HANDLER
# -----------------------------
def handle_pending(job, wait_mins):
    total_nodes, idle_nodes = get_cluster_nodes()
    need = job["nodes"]

    ptype = classify_pending(job, total_nodes, idle_nodes)

    print(f"\n[Detector] Job {job['id']} pending for {wait_mins} minutes")
    print(f"Reason: {job['reason']}")
    print(f"Cluster: {idle_nodes}/{total_nodes} idle")
    print(f"Job needs {need} nodes")

    # INVALID PARAMETERS
    if ptype == "PENDING_INVALID":
        print("→ This job will NEVER run due to invalid parameters.")
        print("→ Sending to Agent-3 for What/Why/Fix analysis.")
        state = load_state()
        state["agent3_request"] = {
            "job_id": job["id"],
            "event": "INVALID_PARAMETERS"
        }
        save_state(state)
        return

    # RESOURCE SHORTAGE
    if ptype == "PENDING_SHORTAGE":
        shortage = max(need - idle_nodes, 0)
        print(f"→ Node Shortage Detected: need {need}, idle {idle_nodes}")
        print(f"Shortfall: {shortage} nodes")

        ans = input("Do you want to burst cloud nodes? (y/n): ").strip().lower()
        if ans != "y":
            print("→ User rejected cloud burst.")
            return

        state = load_state()
        state["agent2_request"] = {
            "job_id": job["id"],
            "shortfall": shortage,
            "event": "CLOUD_BURST_REQUESTED"
        }
        save_state(state)
        print("→ Cloud burst request sent to Agent-2.")
        return

    # QUEUE WAIT
    if ptype == "PENDING_QUEUE_WAIT":
        print("→ Nodes are busy. Cluster CAN run this job.")
        ans = input("Burst cloud nodes anyway? (wait/burst): ").strip().lower()
        if ans != "burst":
            print("→ User chose to wait.")
            return

        state = load_state()
        state["agent2_request"] = {
            "job_id": job["id"],
            "shortfall": 0,
            "event": "USER_FORCED_BURST"
        }
        save_state(state)
        print("→ Cloud burst forced by user.")
        return

    print("→ No action required.")


# -----------------------------
# MAIN LOOP
# -----------------------------
def main():
    print("\n🚀 AGENT-1 DETECTOR V2 — CRASH PROOF\n")

    processed = set()

    while True:
        try:
            jobs = get_jobs()

            for job in jobs:
                jid = job["id"]

                if jid not in processed:
                    processed.add(jid)

                    # FAILED
                    if job["status"] == "F":
                        print(f"\n[Detector] Job {jid} FAILED → Sending to Agent-3")
                        state = load_state()
                        state["agent3_request"] = {
                            "job_id": jid,
                            "event": "FAILED_JOB"
                        }
                        save_state(state)
                        continue

                    # PENDING
                    if job["status"] == "PD":
                        wait = get_timestamp_minutes(job["submit"])
                        if wait >= PENDING_THRESHOLD:
                            handle_pending(job, wait)
                        continue

                    # SUSPENDED
                    if job["status"] == "S":
                        print(f"\n[Detector] Job {jid} Suspended → Sending to Agent-3")
                        state = load_state()
                        state["agent3_request"] = {
                            "job_id": jid,
                            "event": "SUSPENDED_JOB"
                        }
                        save_state(state)
                        continue

                    # COMPLETED
                    if job["status"] == "CD":
                        print(f"[Detector] Job {jid} completed.")
                        continue

        except Exception as e:
            print(f"\n❌ Detector Error: {e}")

        time.sleep(5)


if __name__ == "__main__":
    print("🔥 Detector agent starting...")
    main()