# -*- coding: utf-8 -*-
"""
Created on Mon Oct 27 15:06:36 2025

@author: SREEKANTHVS
"""

import os
import wfdb
import numpy as np
import matplotlib.pyplot as plt
from scipy import signal
from sklearn.preprocessing import StandardScaler

# === Configuration ===
input_folder = r"C:/research_work_DIMAAG_AI_SSE/work_progress_reports/work_report_2025_2026/my_projects/AUTOMATIC_AGING/DATASETS/AA_DATASETS"       # Folder with .dat/.hea files
output_folder = r"C:/research_work_DIMAAG_AI_SSE/work_progress_reports/work_report_2025_2026/my_projects/AUTOMATIC_AGING/RESULTS/time_series"
os.makedirs(output_folder, exist_ok=True)

lowcut, highcut = 1.0, 2.0                   # Frequency band (Hz)
nperseg = 1024                               # Window length for FFT

# === Read PhysioNet .dat file ===
def read_dat_file(filepath):
    base = os.path.splitext(filepath)[0]
    try:
        record = wfdb.rdrecord(base)
        data = record.p_signal
        fs = record.fs
        print(f"Loaded {os.path.basename(filepath)} using wfdb (fs={fs} Hz)")
        return data, fs
    except Exception as e:
        print(f"⚠️ wfdb failed for {filepath}: {e}")
        data = np.loadtxt(filepath)
        fs = 1000  # fallback
        return data, fs

# === Main processing loop ===
for file in os.listdir(input_folder):
    if file.endswith(".dat"):
        filepath = os.path.join(input_folder, file)
        data, fs = read_dat_file(filepath)

        # Normalize each channel
        scaler = StandardScaler()
        data = scaler.fit_transform(data)

        n_channels = data.shape[1] if data.ndim > 1 else 1
        time = np.arange(data.shape[0]) / fs

        # === 1️⃣ Plot and Save Time-Series ===
        colors=['r', 'b', 'k']
        plt.figure(figsize=(10, 6))
        for i in range(n_channels):
            plt.subplot(n_channels, 1, i + 1)
            plt.plot(time[1:10000], data[1:10000, i], linewidth=0.8, color=colors[i])
            plt.title(f"{file} — Channel {i+1}")
            plt.ylabel("Amplitude (Normalized)")
            plt.xlabel("Time (s)")
            plt.grid(True, alpha=0.3)
        plt.tight_layout()
        time_plot_path = os.path.join(output_folder, file.replace(".dat", "_timeseries.png"))
        plt.savefig(time_plot_path, dpi=300)
        plt.close()
        print(f"✅ Saved time-series plot: {time_plot_path}")

