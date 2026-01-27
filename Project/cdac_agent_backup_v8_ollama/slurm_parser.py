import subprocess
import os
import datetime
from config import CLUSTER_CONFIG

def get_wait_time(submit_time_str):
    try:
        fmt = "%Y-%m-%dT%H:%M:%S"
        submit_dt = datetime.datetime.strptime(submit_time_str, fmt)
        diff = datetime.datetime.now() - submit_dt
        return round(diff.total_seconds() / 60, 1)
    except: return 0

def get_idle_node_count():
    try:
        cmd = "sinfo -h -o '%t %D'"
        output = subprocess.check_output(cmd, shell=True).decode('utf-8').strip()
        idle_count = 0
        if output:
            for line in output.split('\n'):
                parts = line.split()
                if len(parts) >= 2 and 'idle' in parts[0].lower():
                    idle_count += int(parts[1])
        return idle_count
    except: return 0

def get_current_jobs():
    jobs = []
    # 1. Fetch Live Jobs (squeue)
    try:
        cmd = ["squeue", "-h", "-o", "%i|%t|%r|%D|%C|%m|%Q|%V"]
        live_out = subprocess.check_output(cmd).decode('utf-8').strip()
        idle_now = get_idle_node_count()
        if live_out:
            for line in live_out.split('\n'):
                p = line.split('|')
                jobs.append({'id': p[0], 'status': p[1], 'reason': p[2], 'nodes': int(p[3]), 
                             'cpus': int(p[4]), 'mem_gb': p[5], 'wait_min': get_wait_time(p[7]), 
                             'idle_now': idle_now})
    except: pass

    # 2. Fetch Historical Jobs from last 2 hours (sacct)
    try:
        start_time = (datetime.datetime.now() - datetime.timedelta(hours=2)).strftime("%H:%M:%S")
        cmd = ["sacct", "-S", start_time, "--format=JobID,State,ExitCode", "-n", "-p"]
        hist_out = subprocess.check_output(cmd).decode('utf-8').strip()
        if hist_out:
            for line in hist_out.split('\n'):
                p = line.split('|')
                if p[1] in ['FAILED', 'TIMEOUT', 'OUT_OF_MEMORY', 'CANCELLED']:
                    if not any(j['id'] == p[0].split('.')[0] for j in jobs):
                        jobs.append({'id': p[0].split('.')[0], 'status': 'FAILED', 'reason': p[2], 
                                     'nodes': 1, 'cpus': 1, 'mem_gb': '0', 'wait_min': 0, 'idle_now': 0})
    except: pass
    return jobs

def get_log_content(job_id):
    path = os.path.join(CLUSTER_CONFIG["STORAGE"]["OUTPUT_PATH"], f"slurm-{job_id}.out")
    if os.path.exists(path):
        with open(path, 'r') as f: return f.read()[-800:]
    return "LOG_NOT_FOUND"