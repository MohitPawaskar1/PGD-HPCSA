CLUSTER_CONFIG = {
    "MAX_LOCAL_NODES": 3,
    "NODE_NAMES": [
        "compute1", 
        "compute2", 
        "compute3"
    ],
    "STORAGE": {
        "OUTPUT_PATH": "/home/acts/project/slurm_ai_agent/logs"
    }
}

AI_CONFIG = {
    "MODEL_ID": "cdac-expert",  # your fine-tuned phi4-mini
    "URL": "http://127.0.0.1:11434/api/generate",
    "TIMEOUT": 60
}