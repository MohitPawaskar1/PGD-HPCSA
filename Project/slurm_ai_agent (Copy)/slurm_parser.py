import subprocess, os, datetime
from config import CLUSTER_CONFIG

def get_wait_time(t):
    try:
        dt = datetime.datetime.strptime(t, "%Y-%m-%dT%H:%M:%S")
        return round((datetime.datetime.now() - dt).total_seconds() / 60, 1)
    except:
        return 0

def get_current_jobs():
    try:
        out = subprocess.check_output(
            "squeue -h -o '%i|%t|%R|%D|%V'", shell=True
        ).decode().strip().split("\n")
    except subprocess.CalledProcessError:
        return []

    jobs = []
    for l in out:
        if not l: continue
        parts = l.split("|")
        if len(parts) < 5: continue

        jid, st, reason, nodes, submit = parts
        jobs.append({
            "id": int(jid),
            "status": st,
            "reason": reason,
            "nodes": int(nodes),
            "submit_time": submit
        })

    return jobs

def get_log_content(job_id):
    log_path = f"{CLUSTER_CONFIG['STORAGE']['OUTPUT_PATH']}/{job_id}.out"

    if not os.path.exists(log_path):
        return "ERROR: LOG_NOT_FOUND"

    try:
        with open(log_path, 'r') as f:
            txt = f.read().strip()
    except Exception:
        return "ERROR: CANNOT_READ_LOG"

    if not txt:
        return "ERROR: LOG_EMPTY"

    if "Traceback" in txt:
        lines = txt.split("\n")
        trace = [l for l in lines if 'File "' in l or "Error" in l]
        return "DETECTED_TRACEBACK: " + " | ".join(trace[-3:])

    # Return the last 600 characters for context
    return txt[-600:]