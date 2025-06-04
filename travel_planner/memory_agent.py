
import json
import os
from datetime import datetime

# Path to memory file
MEMORY_FILE = os.path.join(os.path.dirname(__file__), "memory.json")

def load_memory():
    """Return the stored memory entry or None if file does not exist."""
    if not os.path.isfile(MEMORY_FILE):
        return None
    with open(MEMORY_FILE, "r", encoding="utf-8") as f:
        return json.load(f)

def save_memory(goal: str, plan: list, summary: str):
    """
    Overwrite memory.json with a new entry.
    plan: List of (step: str, result: str) tuples.
    """
    entry = {
        "goal": goal,
        "plan": [{"step": s, "result": r} for s, r in plan],
        "summary": summary,
        "timestamp": datetime.now().isoformat()
    }
    with open(MEMORY_FILE, "w", encoding="utf-8") as f:
        json.dump(entry, f, ensure_ascii=False, indent=2)