from ai_engine import ask_ai
from config import CLUSTER_CONFIG

def analyze_job(job, log_text, wait_minutes):
    """
    Central rule engine for job analysis.
    Runs static rules first, then AI deep analysis.
    """

    jid        = job["id"]
    state      = job["status"]
    reason     = job["reason"]
    nodes      = job["nodes"]

    # ---------------------------------------------------
    # RULE 1: Completed job → no analysis needed
    # ---------------------------------------------------
    if state in ["CD", "COMPLETED"]:
        return {
            "what": "Job completed",
            "why": "Execution finished without errors",
            "fix": "No action needed"
        }

    # ---------------------------------------------------
    # RULE 2: Pending too long → Cloud burst suggestion
    # ---------------------------------------------------
    if state == "PD" and wait_minutes >= CLUSTER_CONFIG["MAX_JOB_WAIT_MINUTES"]:
        return {
            "what": "Job pending too long",
            "why": f"Waiting {wait_minutes} minutes; insufficient cluster nodes",
            "fix": "Burst cloud nodes to satisfy resource requirement"
        }

    # ---------------------------------------------------
    # RULE 3: Suspended
    # ---------------------------------------------------
    if state == "S":
        return {
            "what": "Suspended job",
            "why": f"Job is in SUSPENDED state ({reason})",
            "fix": f"Resume using: scontrol resume {jid}"
        }

    # ---------------------------------------------------
    # RULE 4: Admin Hold
    # ---------------------------------------------------
    if state == "PD" and "hold" in reason.lower():
        return {
            "what": "Job on hold",
            "why": f"Admin hold: {reason}",
            "fix": f"Release using: scontrol release {jid}"
        }

    # ---------------------------------------------------
    # RULE 5: If basic rules don’t match → send to AI
    # ---------------------------------------------------
    ai_result = ask_ai(
        jid,
        state,
        reason,
        nodes,
        wait_minutes,
        log_text
    )

    return ai_result