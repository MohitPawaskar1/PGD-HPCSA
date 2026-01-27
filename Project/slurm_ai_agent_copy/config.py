CLUSTER_CONFIG = {
    "MAX_CLUSTER_NODES": 3,               # local compute nodes
    "MAX_JOB_WAIT_MINUTES": 5,            # pending limit
    "LOG_PATH": "/home/acts/project/fail_jobs"
}



AI_CONFIG = {
    "MODEL_ID": "phi3:instruct",
    "URL": "http://127.0.0.1:11434/api/generate",
    "TIMEOUT": 45
}