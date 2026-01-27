import json
import requests
from config import CLUSTER_CONFIG

# -----------------------------------------------------------
# STRICT JSON ENFORCING SYSTEM PROMPT
# -----------------------------------------------------------

AI_SYSTEM_PROMPT = """
You are the CDAC SLURM Diagnostic AI.

You MUST reply ONLY in valid JSON.
No explanations. No markdown. No code fences. No extra text.

Your JSON MUST follow this EXACT format:

{
  "what": "<one short line>",
  "why": "<one short line>",
  "fix": "<one short actionable fix>"
}

RULES:
- Output ONLY the JSON object, nothing else.
- No text before the JSON.
- No text after the JSON.
- No backticks.
- No blank lines before or after.
- Never include multiple JSON blocks.
- Keep each value short and crisp (max 1 sentence).
"""

# -----------------------------------------------------------
# OLLAMA REQUEST FUNCTION (SAFE STREAMING & JSON CLEANING)
# -----------------------------------------------------------

def ask_ai(job_id, job_state, job_reason, job_nodes, wait_minutes, log_text):
    """
    Sends SLURM job details & logs to the AI model
    and enforces strict JSON response.
    """

    # USER PROMPT
    user_prompt = f"""
Analyze this SLURM job and return ONLY the JSON object.

Job ID: {job_id}
State: {job_state}
Reason: {job_reason}
Nodes: {job_nodes}
Pending Minutes: {wait_minutes}

Log Snippet:
{log_text}

Return strictly the JSON object described by the system prompt.
"""

    payload = {
        "model": CLUSTER_CONFIG["AI_MODEL"],
        "prompt": AI_SYSTEM_PROMPT + "\n\n" + user_prompt,
        "stream": True
    }

    try:
        response = requests.post(
            CLUSTER_CONFIG["OLLAMA_URL"] + "/api/generate",
            json=payload,
            stream=True,
            timeout=120
        )

        raw = ""
        for chunk in response.iter_lines():
            if not chunk:
                continue
            try:
                part = json.loads(chunk.decode("utf-8"))
                if "response" in part:
                    raw += part["response"]
            except:
                continue

        cleaned = clean_json_output(raw)
        return json.loads(cleaned)

    except Exception as e:
        return {
            "what": "AI error",
            "why": str(e),
            "fix": "Check model or network"
        }

# -----------------------------------------------------------
# JSON CLEANER (STRIPS ALL NON-JSON CONTENT)
# -----------------------------------------------------------

def clean_json_output(text):
    """
    Extracts the first valid JSON object from model output.
    Removes:
    - backticks
    - markdown
    - text before JSON
    - text after JSON
    """

    # Remove forbidden characters
    text = text.replace("```", "").replace("json", "").strip()

    # Find JSON boundaries
    start = text.find("{")
    end = text.rfind("}")

    if start == -1 or end == -1:
        return '{"what":"AI error","why":"Invalid JSON","fix":"Re-run analysis"}'

    cleaned = text[start:end+1]

    # Validate JSON format
    try:
        json.loads(cleaned)
        return cleaned
    except:
        return '{"what":"AI error","why":"JSON parse fail","fix":"Check prompt"}'