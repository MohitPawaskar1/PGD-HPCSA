# config.py

# --- 1. LOCAL PHYSICAL CLUSTER CONFIG ---
# Your on-premise hardware limits
CLUSTER_CONFIG = {
    "MAX_LOCAL_NODES": 3,
    "CPUS_PER_NODE": 16,
    "RAM_PER_NODE_GB": 40,
    "NODE_NAMES": ["compute1", "compute2", "compute3"],
    
    # Storage & NFS Architecture
    "STORAGE": {
        "NFS_SERVER": "compute2",
        "INPUT_PATH": "/storage/input",
        "OUTPUT_PATH": "/storage/output",
        # List for health-check loops
        "MOUNT_POINTS": ["/storage/input", "/storage/output"]
    }
}

# --- 2. DYNAMIC CLOUD BURSTING CONFIG ---
# Define a menu so the agent can "shop" for the best fit
CLOUD_INSTANCES = [
    {"name": "t3.medium",  "cpus": 2,  "ram_gb": 4},   # Small/Default
    {"name": "t3.large",   "cpus": 2,  "ram_gb": 8},   # Memory-heavy small
    {"name": "c5.xlarge",  "cpus": 4,  "ram_gb": 8},   # Compute optimized
    {"name": "m5.2xlarge", "cpus": 8,  "ram_gb": 32},  # Balanced large
    {"name": "r5.2xlarge", "cpus": 8,  "ram_gb": 64},  # Memory optimized
]

CLOUD_LIMITS = {
    "PROVIDER": "AWS",
    "MAX_BURST_NODES": 10,
    "REGION": "us-east-1"
}

# --- 3. AI AGENT SETTINGS ---
AI_CONFIG = {
    "MODEL_ID": "cdac-expert-v7",
    "URL": "http://compute2:11434/api/generate",
    "TIMEOUT": 30
}