#!/usr/bin/env python3
"""
host_agent.py - defensive skeleton for monitoring HID-like typing behavior.
This skeleton is educational and intentionally does NOT capture keystrokes
or perform invasive behavior. Instead it provides hooks and examples to
process timing data that a *consenting* test application could provide.
"""

import time
import math
import json
from statistics import mean, pstdev

def host_score_from_mean_iki(mean_iki_ms: float) -> float:
    """
    Simple sigmoid mapping: faster (smaller) IKIs -> higher anomaly score.
    Defensive example only.
    """
    # Sigmoid centered around 80 ms
    return 1.0 / (1.0 + math.exp((mean_iki_ms - 80.0) / 15.0))

def compute_session_score(iki_list_ms):
    if not iki_list_ms:
        return 0.0
    m = mean(iki_list_ms)
    s = pstdev(iki_list_ms) if len(iki_list_ms) > 1 else 0.0
    score = host_score_from_mean_iki(m)
    return max(0.0, min(1.0, score))

def report_event(server_url, payload):
    # placeholder: in your deployment use HTTPS and authentication
    print("REPORT to", server_url, "payload:", json.dumps(payload))

if __name__ == "__main__":
    # Demo usage with simulated IKIs (do not run on third-party machines)
    simulated_human_iki = [180, 220, 170, 200, 190, 210]
    simulated_auto_iki = [30, 32, 29, 31, 33, 30]
    print("Human session score:", compute_session_score(simulated_human_iki))
    print("Automation session score:", compute_session_score(simulated_auto_iki))
    # Example payload
    payload = {
        "host_id": "host1",
        "session_id": "demo-001",
        "host_score": compute_session_score(simulated_auto_iki),
        "timestamp": time.time()
    }
    report_event("https://logger.local/api/events", payload)
