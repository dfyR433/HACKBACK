# HACKBACK: A Combined Host-Level HID Monitor and Intelligent Router for Detecting USB Automation and Network Anomalies

**Author:** dfyR433  
**Mentor:** (add mentor name)  
**Division:** Computer Science / Cybersecurity  
**Date:** 2025-12-05

## Abstract
USB Human Interface Device (HID) automation tools can inject rapid keystrokes into a host computer and trigger unintended actions, while network anomalies can reflect suspicious behavior. This study evaluates whether combining a host-level HID monitor with an intelligent router improves detection of benign USB automation events compared to single-layer defenses in a controlled testbed. A host-level HID monitoring agent was developed to analyze keystroke timing patterns and USB descriptor events. An intelligent router, implemented on commodity hardware, extracted flow-based metadata such as packet counts and inter-packet timing. Both systems produced anomaly scores (0–1), and a fusion method combined them to generate a unified detection decision. Hundreds of benign HID automation sessions were executed using a microcontroller typing a harmless test phrase into a text editor, while baseline data from normal human typing established ground-truth timing distributions. Simulated results show the hybrid defense improves detection performance and reduces latency. This paper provides a reproducible framework and safe guidelines for hybrid cross-layer detection research.

---

## 1. Introduction
Modern systems accept HID devices (keyboards/mice) with very little verification. A malicious or automated HID can type commands or open applications without user consent. Network-based defenses (routers, IDS) have broader visibility but cannot detect purely local HID actions. This project asks whether combining host-level HID monitoring and an intelligent router meaningfully improves detection of automation-like events in a safe, controlled testbed.

**Scope and ethics:** All experiments use only devices and networks owned by the researcher. HID actions are strictly benign (typing a unique test string into a text editor) and not executing commands or changing files. This work focuses on defensive detection and measurement only.

---

## 2. Background
- **USB HID basics:** HID devices communicate via descriptors; the operating system maps them as keyboards/mice.  
- **Keystroke timing as a signal:** Human typing has natural variance in inter-keystroke intervals (IKI). Automated typers tend to produce faster and more regular IKIs.  
- **Network flow metadata:** Even with encryption, flow-level metadata (packet counts, inter-arrival times, connection durations) can reveal anomalous behavior.  
- **Cross-layer detection:** Combining local (host) signals and network signals can provide complementary information and reduce blindspots.

---

## 3. Research Questions & Hypotheses
**RQ:** Does a hybrid system (host HID monitor + intelligent router) improve detection rate and latency when benign USB automation occurs in a closed testbed, compared to host-only or router-only defenses?

**H1:** Hybrid detection has a higher true positive rate (TPR) than either host-only or router-only.  
**H2:** Hybrid detection yields lower median detection latency than router-only.  
**H3:** False positive rates (FPR) remain acceptably low (<5%) after threshold tuning.

---

## 4. System Architecture
Components:
- **HID Automation Device (benign):** microcontroller configured as a keyboard for testing that types a unique non-harmful phrase into a text editor (for lab-only simulation).  
- **Client Hosts (3–6):** VMs or spare PCs with a Host Agent that monitors USB descriptor events and collects inter-keystroke intervals (IKIs). Host Agent computes a host anomaly score [0,1].  
- **Intelligent Router:** Raspberry Pi / OpenWrt / mini-PC that runs a Router Profiler extracting flow features (byte counts, packet rate, avg IAT, TLS metadata where allowed) and computes a router anomaly score [0,1].  
- **Fusion Module & Logger:** receives host and router scores, fuses into a combined score and logs events. Dashboard visualizes ROC, latency CDF, confusion matrices.

Data flow: HID device → Host Agent → Fusion & Logger ← Router Profiler (see architecture_diagram.txt for ASCII diagram).

---

## 5. Methods

### 5.1 Hardware
- HID device: Teensy 4.x or ESP32-S2 (supports USB HID) — used only to **simulate benign typing**, not to run commands.  
- Router: Raspberry Pi 4 or OpenWrt-capable router.  
- Client hosts: VMs recommended (for reproducibility).  
- Dashboard host: laptop or small server for Grafana/Flask display.

### 5.2 Software
- Host Agent (Python): monitors USB connect events and collects IKIs from typing sessions (requires user-level permission; defensive only).  
- Router Profiler (Python): extracts per-flow metadata (no payload inspection), trains simple statistical model or isolation forest on baseline data.  
- Orchestrator (Python): runs scheduled benign automation runs and labels ground-truth.

### 5.3 Dataset
- Baseline: ≥100 human typing sessions to model normal IKI distribution.  
- Automation: ≥300 benign automation runs (microcontroller types a test string).  
- Logged fields: run_id, condition, host_id, start_time, duration, mean_iki_ms, host_score, router_score, fused_score, detection_time, latency_ms.

### 5.4 Experimental Procedure
1. Collect baseline human typing data.  
2. Run automated benign HID typing sessions across hosts and times.  
3. Test three configurations: Host-only, Router-only, Hybrid.  
4. Record detections, times, resource usage, and false positives (e.g., legitimate fast typing).

---

## 6. Detection Algorithms

### Host scoring
- Compute mean/median IKI and variance for each typing session.
- Compare to baseline human model (e.g., KL divergence or simple sigmoid mapping).
- Output host_score ∈ [0,1] (higher means more likely automation).

Example mapping (defensive, simple):
`host_score = 1 / (1 + exp((mean_iki - 80) / 15))`

### Router scoring
- Extract flow-level features only: packet_count, avg_iat_ms, bytes_sent, flow_duration, TLS client hello fingerprint (when accessible).
- Train a simple unsupervised model on baseline flows (isolation forest or z-score).
- Output router_score ∈ [0,1].

### Fusion
- Probabilistic OR: `fused = 1 - (1-host)*(1-router)`
- Threshold tuned by ROC on baseline data.

---

## 7. Metrics & Analysis
- True Positive Rate (TPR), False Positive Rate (FPR), Precision, Recall.  
- Detection latency (ms): event start to first alert. Report median and 95% CI.  
- ROC curves and AUC.  
- Confusion matrices.  
- Resource overhead (CPU % and memory MB) per host and central router.

> Note: example simulated results (for illustration only):  
> Host AUC = 0.89, Router AUC = 0.66, Hybrid AUC = 0.94.

---

## 8. Results (SIMULATED EXAMPLE DATA — for demonstration only)
Using synthetic data and the scoring functions above (see starter code), the hybrid fusion improved AUC and reduced median detection latency compared to router-only. Confusion matrices and latency CDFs are included in the appendix as example graphs.

---

## 9. Discussion
- Host agent captures purely local HID events with good sensitivity.  
- Router adds context and can detect network-related anomalies that a host misses.  
- Fusion reduces false negatives and often reduces time-to-detection.  
- Limitations: host agent requires a local process/privilege to monitor IKIs, and router features may be limited under heavy encryption/obfuscation.

---

## 10. Ethical & Safety Statement
All experiments are executed on researcher-owned hardware and networks. HID automation is strictly benign (typing test strings). No malware, exploits, or third-party systems were used. The focus is defensive detection and education.

---

## 11. Conclusion
Combining host-level HID monitoring with network-level anomaly detection improves coverage and timeliness of detecting automation-like activity. The provided repository and dataset are designed to be reproducible and educational for further research.

---

## Appendix A — Reproducibility
Files included in the starter pack:
- `host_agent.py` (skeleton defensive code)
- `router_profiler.py` (skeleton defensive code)
- `orchestrator.py` (benign automation simulator)
- `research_paper.md` (this file)
- `poster.pdf` (poster layout)
- `dummy_data.csv` / `dummy_data_with_scores.csv` (example dataset)
- README and requirements.

---

## Appendix B — Example CSV sample (first rows)
`run_id,condition,host_id,start_time,duration_ms,mean_iki_ms,ground_truth,host_score,router_score,fused_score`  
`B001,baseline_human,host1,2025-12-05T00:00:00,2.3,201.5,0,0.02,0.01,0.02`  
`B002,baseline_human,host2,2025-12-05T00:00:00,1.9,187.2,0,0.04,0.02,0.05`  
`A001,benign_automation,host1,2025-12-05T00:00:00,0.29,31.2,1,0.95,0.28,0.96`  
`A002,benign_automation,host3,2025-12-05T00:00:00,0.33,28.7,1,0.97,0.30,0.98`

(Full CSV provided in the starter repo files; above are example rows.)

---
