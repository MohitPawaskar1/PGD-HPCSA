import requests, time, sys, os
import json
from slurm_parser import get_current_jobs, get_log_content, get_wait_time
from config import CLUSTER_CONFIG, AI_CONFIG

# ------------------------------------------------------------
# 1. RULE-BASED ENGINE (Zero-Mistake Layer)
# ------------------------------------------------------------
def rule_based_diagnosis(job, logs):
    status = job.get("status", "").upper()
    reason = job.get("reason", "").upper()
    jid = job["id"]

    # ADMIN HOLD
    if "HOLD" in reason or "HELD" in reason or status == "H":
        return {
            "what": "Administrative hold",
            "why": "Job was manually held",
            "fix": f"scontrol release {jid}"
        }

    # SUSPENDED
    if status == "S":
        return {
            "what": "Job suspended",
            "why": "Scheduler/admin paused execution",
            "fix": f"scontrol resume {jid}"
        }

    # LONG WAIT (Pending >5 min)
    if status == "PD":
        wt = get_wait_time(job["submit_time"])
        if wt >= 5:
            return {
                "what": "Long pending job",
                "why": f"Pending for {wt} minutes",
                "fix": "Reduce constraints or burst to cloud"
            }

    # COMMAND NOT FOUND / EXIT 127
    if "EXIT 127" in logs.upper() or "COMMAND NOT FOUND" in logs.upper():
        return {
            "what": "Command missing",
            "why": "Executable not in PATH",
            "fix": "Load module or give full path"
        }

    # PYTHON TRACEBACK
    if "DETECTED_TRACEBACK" in logs:
        return {
            "what": "Runtime crash",
            "why": "Python traceback detected",
            "fix": "Fix script syntax"
        }

    # OUT OF MEMORY
    if "OUT OF MEMORY" in logs.upper():
        return {
            "what": "Memory exceeded",
            "why": "Job ran out of RAM",
            "fix": "Increase --mem"
        }

    # TIME LIMIT
    if "TIME LIMIT" in reason:
        return {
            "what": "Time exceeded",
            "why": "Job hit time limit",
            "fix": "Increase --time"
        }

    # SUCCESS
    if status == "CD":
        return {
            "what": "Job completed",
            "why": "Execution finished cleanly",
            "fix": "None"
        }

    return None


# ------------------------------------------------------------
# 2. AI FALLBACK (STRICT SHORT FORMAT)
# ------------------------------------------------------------
def ask_expert_ai(job, logs):
    prompt = f"""
    You are a SLURM job expert.
    Analyze the job and answer ONLY in this exact JSON format:

    {{
    "what": "<max 8 words>",
    "why": "<max 12 words>",
    "fix": "<single command or short fix>"
    }}

    NO extra text. NO explanation. ONLY valid JSON.

    JOB DATA:
    {job}

    LOG OUTPUT:
    {logs}
    """

    payload = {
        "model": AI_CONFIG["MODEL_ID"],
        "prompt": prompt,
    }

    try:
        r = requests.post(AI_CONFIG["URL"], json=payload, timeout=AI_CONFIG["TIMEOUT"])
        raw = r.json().get("response", "").strip()

        # try parsing JSON output
        return json.loads(raw)

    except Exception:
        return {
            "what": "AI error",
            "why": "Model failed to respond",
            "fix": "Check model runtime"
        }


# ------------------------------------------------------------
# 3. PRETTY PRINT BOX
# ------------------------------------------------------------
def print_audit(job_id, result):
    print("\n ╔" + "═" * 70 + "╗")
    print(f" ║ JOB {job_id} DIAGNOSIS{' ' * 50}║")
    print(" ╠" + "═" * 70 + "╣")
    print(f" ║ WHAT: {result['what']:<60}║")
    print(f" ║ WHY : {result['why']:<60}║")
    print(f" ║ FIX : {result['fix']:<60}║")
    print(" ╚" + "═" * 70 + "╝")


# ------------------------------------------------------------
# 4. MAIN LOOP
# ------------------------------------------------------------
def main():
    print("\n🚀 CDAC AI AGENT V16 | Monitoring Active Jobs...\n")

    processed = set()

    while True:
        try:
            jobs = get_current_jobs()

            for job in jobs:
                jid = job["id"]
                if jid in processed:
                    continue

                # CLOUD BURST CHECK
                if job.get("nodes", 0) > CLUSTER_CONFIG["MAX_LOCAL_NODES"]:
                    extra = job["nodes"] - CLUSTER_CONFIG["MAX_LOCAL_NODES"]
                    print(f"\n🚨 Job {jid} needs {extra} more nodes!")
                    ch = input("👉 Burst to cloud? (y/n): ").lower()
                    if ch == "y":
                        print(" ✅ Cloud scaling started.")
                        processed.add(jid)
                        continue

                logs = get_log_content(jid)

                # RULE FIRST
                rule = rule_based_diagnosis(job, logs)
                if rule:
                    print_audit(jid, rule)
                    processed.add(jid)
                    continue

                # AI NEXT
                ai = ask_expert_ai(job, logs)
                print_audit(jid, ai)
                processed.add(jid)

        except Exception as e:
            print(f"\n❌ Agent error: {e}")

        time.sleep(10)


if __name__ == "__main__":
    main()