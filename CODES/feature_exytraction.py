# -*- coding: utf-8 -*-
"""
Created on Tue Oct 28 11:13:14 2025

@author: SREEKANTHVS
"""

# =============================================================
# Autonomic Aging (PhysioNet) – ECG + BP Analysis Notebook
# Author: ChatGPT (GPT-5)
# =============================================================

# --- Imports ---
import os
import wfdb
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from scipy.signal import butter, filtfilt, find_peaks
from scipy.stats import linregress

# =============================================================
# 1. Load Metadata
# =============================================================
# Assumes dataset is downloaded from PhysioNet into ./autonomic-aging-cardiovascular-1.0.0
# You can download via:
# !wget -r -N -c -np https://physionet.org/files/autonomic-aging-cardiovascular/1.0.0/

base_path = "C:/research_work_DIMAAG_AI_SSE/work_progress_reports/work_report_2025_2026/my_projects/AUTOMATIC_AGING/DATASETS/AA_DATASETS"
meta_path = os.path.join(base_path, "subject-info.csv")
metadata = pd.read_csv(meta_path)
print("Metadata loaded:", metadata.shape)
metadata.head()
metadata["ID"] = metadata["ID"].apply(lambda x: str(int(float(x))).zfill(4))

# =============================================================
# 2. Load One Record (ECG + BP)
# =============================================================
record_id = metadata.iloc[0]['ID']  # or 'record_name' depending on CSV
record_path = os.path.join(base_path, str(record_id))
record = wfdb.rdrecord(record_path)
signals = record.p_signal
fs = record.fs
sig_names = record.sig_name

print(f"Loaded record: {record_id}")
print(f"Channels: {sig_names}, Sampling Rate: {fs} Hz")

# Assume 0 = ECG, 1 = Blood Pressure
ecg = signals[:, 0]
bp = signals[:, 1]

# =============================================================
# 3. Preprocessing (Filtering)
# =============================================================
def bandpass_filter(sig, fs, low=0.5, high=40):
    b, a = butter(2, [low/(fs/2), high/(fs/2)], btype='band')
    return filtfilt(b, a, sig)

ecg_filt = bandpass_filter(ecg, fs)
bp_filt = filtfilt(*butter(2, [0.1/(fs/2), 20/(fs/2)], btype='band'), bp)

# =============================================================
# 4. ECG Peak Detection and HRV
# =============================================================
rpeaks, _ = find_peaks(ecg_filt, distance=int(0.6*fs), height=np.std(ecg_filt)*2)
rr_intervals = np.diff(rpeaks) / fs * 1000  # in ms

def compute_hrv_features(rr):
    rr_mean = np.mean(rr)
    sdnn = np.std(rr)
    rmssd = np.sqrt(np.mean(np.diff(rr)**2))
    return {"RR_mean_ms": rr_mean, "SDNN_ms": sdnn, "RMSSD_ms": rmssd}

hrv_features = compute_hrv_features(rr_intervals)
print("HRV Features:", hrv_features)

# =============================================================
# 5. BP Feature Extraction (Systolic / Diastolic)
# =============================================================
systolic_peaks, _ = find_peaks(bp_filt, distance=int(0.5*fs))
diastolic_peaks, _ = find_peaks(-bp_filt, distance=int(0.5*fs))

sbp = bp_filt[systolic_peaks]
dbp = bp_filt[diastolic_peaks]
bp_features = {
    "SBP_mean": np.mean(sbp),
    "DBP_mean": np.mean(dbp),
    "BP_variability": np.std(sbp)
}
print("BP Features:", bp_features)

# =============================================================
# 6. Baroreflex Sensitivity (BRS)
# =============================================================
# Simple sequence method (RR vs SBP)
min_len = min(len(rr_intervals), len(sbp)-1)
if min_len > 0:
    rr_seq = rr_intervals[:min_len]
    sbp_seq = sbp[1:min_len+1]
    slope, r_val, _, _, _ = linregress(sbp_seq, rr_seq)
    brs = {"BRS_slope": slope, "BRS_r": r_val}
else:
    brs = {"BRS_slope": np.nan, "BRS_r": np.nan}
print("Baroreflex:", brs)

# =============================================================
# 7. Save Features
# =============================================================
features = {**hrv_features, **bp_features, **brs}
features["ID"] = record_id
features_df = pd.DataFrame([features])
out_csv = "autonomic_aging_features.csv"
features_df.to_csv(out_csv, index=False)
print(f"✅ Features saved to {out_csv}")

# =============================================================
# 8. Visualization
# =============================================================
plt.figure(figsize=(12, 5))
plt.subplot(2,1,1)
plt.plot(ecg_filt[:10_000])
plt.title("Filtered ECG (first 10 seconds)")
plt.subplot(2,1,2)
plt.plot(bp_filt[:10_000])
plt.title("Filtered BP (first 10 seconds)")
plt.tight_layout()
plt.show()
