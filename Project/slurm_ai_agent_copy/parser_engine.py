import subprocess, os, datetime
from config import CLUSTER_CONFIG

# -----------------------------------------------------------
# 1. WAIT TIME CALCULATOR
# -----------------------------------------------------------
def get_wait_time(ts):
    try:
        t = datetime.datetime.strptime(ts, "%Y-%m-%dT%H:%M:%S")
        return round((datetime.datetime.now() - t).total_seconds() / 60, 1)
    except:
        return 0


# -----------------------------------------------------------
# 2. CURRENT JOB FETCHER (from squeue)
# -----------------------------------------------------------
def get_current_jobs():
    out = subprocess.getoutput("squeue -h -o '%i|%t|%R|%D|%V'")
    jobs = []

    for line in out.split("\n"):
        if "|" not in line:
            continue
        jid, st, reason, nodes, submit = line.split("|")
        jobs.append({
            "id": int(jid),
            "status": st,
            "reason": reason,
            "nodes": int(nodes),
            "submit_time": submit
        })
    return jobs


# -----------------------------------------------------------
# 3. LOG FETCHER (FIXED FOR YOUR ENV)
# -----------------------------------------------------------
def get_log_content(job_id):
    """
    SLURM logs for your setup follow this pattern:
    /home/acts/project/fail_jobs/slurm-<jobid>.out
    """

    log_path = os.path.join(
        CLUSTER_CONFIG["LOG_PATH"],
        f"slurm-{job_id}.out"
    )

    # Check existence
    if not os.path.exists(log_path):
        return "ERROR: LOG_NOT_FOUND"

    # Read log content
    try:
        txt = open(log_path).read().strip()
    except:
        return "ERROR: LOG_READ_FAIL"

    if not txt:
        return "ERROR: LOG_EMPTY"

    # Detect Python Traceback
    if "Traceback" in txt:
        lines = txt.split("\n")
        trace = [l for l in lines if "File \"" in l or "Error" in l]
        return "DETECTED_TRACEBACK: " + " | ".join(trace[-3:])

    # Return last 1500 chars for efficient AI processing
    return txt[-1500:]