#!/usr/bin/env python3
"""
router_profiler.py - defensive skeleton to compute simple flow-level features
and an anomaly score. This script expects pre-parsed flow metadata (no payload
inspection). It demonstrates feature extraction and a placeholder scoring function.
"""

import math
import json
from statistics import mean

def extract_flow_features(flow_meta):
    """
    Example flow_meta dictionary keys expected:
    - 'packet_count', 'bytes', 'duration_ms', 'avg_iat_ms'
    This function standardizes and returns the numeric feature vector.
    """
    packet_count = flow_meta.get('packet_count', 0)
    bytes_sent = flow_meta.get('bytes', 0)
    duration = flow_meta.get('duration_ms', 1)
    avg_iat = flow_meta.get('avg_iat_ms', duration / max(1, packet_count))
    return {
        'packet_count': packet_count,
        'bytes': bytes_sent,
        'duration_ms': duration,
        'avg_iat_ms': avg_iat
    }

def simple_router_score(features):
    """
    Example scoring: flows with extremely low avg_iat and high packet rate may be suspicious.
    Return normalized score in [0,1]. This is illustrative only.
    """
    # Heuristics - scale values into 0..1 roughly
    pk_rate = features['packet_count'] / max(1, features['duration_ms'])  # packets per ms
    iat = features['avg_iat_ms']
    # Smaller iat -> higher score
    score = 1.0 / (1.0 + math.exp((iat - 150.0) / 75.0))
    # Factor in packet rate (clamp)
    score = max(0.0, min(1.0, 0.7 * score + min(pk_rate * 0.0005, 0.3)))
    return score

if __name__ == "__main__":
    example_flow = {
        'packet_count': 120,
        'bytes': 15000,
        'duration_ms': 200,
        'avg_iat_ms': 1.6
    }
    feats = extract_flow_features(example_flow)
    print("Features:", feats)
    print("Router score:", simple_router_score(feats))
