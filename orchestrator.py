#!/usr/bin/env python3
"""
orchestrator.py - benign automation simulator (defensive).
This script demonstrates how you might orchestrate tests that simulate
HID typing in a safe way. IMPORTANT: do NOT run code that emulates a real
keyboard on machines you don't own or without consent. This script prints
a simulated run rather than sending real keystrokes.
"""

import time
import uuid

def run_benign_simulation(host_id="host1", n_chars=100, speed_cps=30):
    """
    Simulate a benign HID typing session:
    - n_chars: number of characters typed
    - speed_cps: characters per second (use slow for human-like, fast for automation)
    """
    session_id = str(uuid.uuid4())[:8]
    print(f"[SIM] Starting benign simulation: session={session_id}, host={host_id}")
    # simulate timing list (not actually sending keystrokes)
    if speed_cps <= 60:
        # more human-like variance
        import random
        ikis = [max(20, random.gauss(1000.0/speed_cps, 30)) for _ in range(n_chars)]
    else:
        # automation-like regular fast typing
        ikis = [max(5, 1000.0/speed_cps) for _ in range(n_chars)]
    duration_ms = sum(ikis)
    mean_iki = sum(ikis) / len(ikis)
    print(f"[SIM] session={session_id} mean_iki_ms={mean_iki:.1f} duration_ms={duration_ms:.1f}")
    return {
        'session_id': session_id,
        'host_id': host_id,
        'mean_iki_ms': mean_iki,
        'duration_ms': duration_ms
    }

if __name__ == "__main__":
    # Example runs (no real HID events)
    print(run_benign_simulation("host1", n_chars=80, speed_cps=5))   # human-like
    print(run_benign_simulation("host2", n_chars=80, speed_cps=30))  # automation-like
