from config import CLUSTER_CONFIG

def check_cloud_need(job):
    needed = job["nodes"]
    max_local = CLUSTER_CONFIG["MAX_CLUSTER_NODES"]

    if needed > max_local:
        diff = needed - max_local
        return f"\n🚨 Job {job['id']} needs {diff} extra nodes.\n👉 Burst to cloud needed."

    return None