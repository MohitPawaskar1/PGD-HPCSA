import requests
import time
from slurm_parser import get_current_jobs, get_log_content
from config import CLUSTER_CONFIG, CLOUD_INSTANCES, AI_CONFIG

def main():
    print(f"🚀 CDAC AI AGENT V10.0 | Production Audit")
    processed = set()

    while True:
        jobs = get_current_jobs()
        for job in jobs:
            if job['id'] in processed: continue
            
            # --- SCENARIO 1: CAPACITY BURST (Immediate calculation) ---
            if job['status'] == 'PD' and job['nodes'] > CLUSTER_CONFIG["MAX_LOCAL_NODES"]:
                inst = select_best_instance(job)
                needed = job['nodes'] - CLUSTER_CONFIG["MAX_LOCAL_NODES"]
                print(f"\n--- Investigating Job {job['id']} (Capacity) ---")
                print(f"Requirement: {job['nodes']} nodes | Idle: {job['idle_now']} | Shortfall: {needed}")
                if input(f"👉 Authorize AWS Burst for {needed} x {inst}? (y/n): ").lower() == 'y':
                    print("✅ Scaling Triggered.")
                processed.add(job['id'])

            # --- SCENARIO 2: TECHNICAL FAILURES/HOLD (Immediate WHAT/WHY/FIX) ---
            elif job['status'] in ['FAILED', 'H', 'S', 'TIMEOUT', 'OUT_OF_MEMORY']:
                print(f"\n--- Technical Diagnosis: Job {job['id']} ---")
                print(ask_expert_ai(job, get_log_content(job['id'])))
                processed.add(job['id'])

            # --- SCENARIO 3: STUCK PENDING (Wait > 5 min) ---
            elif job['status'] == 'PD' and job['wait_min'] >= 5.0:
                print(f"\n--- Queue Diagnosis: Job {job['id']} (Stuck {job['wait_min']}m) ---")
                print(ask_expert_ai(job, "LOG_NOT_FOUND"))
                processed.add(job['id'])

        time.sleep(20)

def ask_expert_ai(job, logs):
    prompt = f"ID:{job['id']} STAT:{job['status']} REASON:{job['reason']} WAIT:{job['wait_min']}m LOGS:{logs}"
    payload = {"model": AI_CONFIG["MODEL_ID"], "prompt": prompt, "stream": False, "context": []}
    try:
        r = requests.post(AI_CONFIG["URL"], json=payload, timeout=30)
        return r.json().get('response', 'AI_ERR').strip()
    except: return "AI_OFFLINE"

def select_best_instance(job):
    # Match logic...
    return "m5.4xlarge"

if __name__ == "__main__": main()