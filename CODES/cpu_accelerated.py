# -*- coding: utf-8 -*-
"""
Created on Mon Oct 27 19:17:43 2025

@author: SREEKANTHVS
"""

import os
import numpy as np
import matplotlib.pyplot as plt
from scipy import signal
from joblib import Parallel, delayed
from numba import njit, prange

# Try to import wfdb for PhysioNet .dat files
try:
    import wfdb
    USE_WFDB = True
except ImportError:
    USE_WFDB = False
    print("⚠️ wfdb not found. Install with 'pip install wfdb' if using PhysioNet .dat files.")

# === CONFIGURATION ===
input_folder = r"C:\research_work_DIMAAG_AI_SSE\work_progress_reports\work_report_2025_2026\my_projects\AUTOMATIC_AGING\DATASETS\AA_DATASETS"
output_folder = r"C:\research_work_DIMAAG_AI_SSE\work_progress_reports\work_report_2025_2026\my_projects\AUTOMATIC_AGING\RESULTS\filtered_spectrograms"
default_fs = 1000  # Hz
os.makedirs(output_folder, exist_ok=True)

# === FAST SIGNAL NORMALIZATION ===
@njit(parallel=True, fastmath=True)
def normalize_signal_numba(data):
    """Normalize each channel (zero mean, unit variance) using Numba for speed."""
    n_samples, n_channels = data.shape
    for ch in prange(n_channels):
        mean = np.mean(data[:, ch])
        std = np.std(data[:, ch]) + 1e-8
        data[:, ch] = (data[:, ch] - mean) / std
    return data


# === READ PHYSIONET OR FALLBACK ===
def read_dat_file(filepath):
    base = os.path.splitext(filepath)[0]

    if USE_WFDB and os.path.exists(base + ".hea"):
        try:
            record = wfdb.rdrecord(base)
            data = record.p_signal
            fs = record.fs
            print(f"  -> Loaded {data.shape[0]} samples, {data.shape[1]} channels, fs={fs} Hz")
            return data, fs
        except Exception as e:
            print(f"⚠️ WFDB failed for {filepath}: {e}")

    # Fallback: try ASCII or binary float32
    try:
        data = np.loadtxt(filepath)
        fs = default_fs
    except Exception:
        data = np.fromfile(filepath, dtype=np.float32)
        data = data.reshape(-1, 1)  # assume single channel if not rectangular
        fs = default_fs

    print(f"  -> Loaded {data.shape[0]} samples (fallback mode), fs={fs} Hz")
    return data, fs


# === COMPUTE NORMALIZED PSD SPECTROGRAM (1–2 Hz FILTERED) ===
def compute_normalized_spectrogram(data, fs=1000, nperseg=1024):
    f, t, Sxx = signal.spectrogram(data, fs=fs, nperseg=nperseg, noverlap=nperseg // 2)

    # Normalize Power Spectral Density
    Sxx_sum = np.sum(Sxx, axis=0, keepdims=True) + 1e-12
    Sxx_norm = Sxx / Sxx_sum

    # Frequency-domain filtering: retain only 1–2 Hz
    freq_mask = (f >= 1.0) & (f <= 2.0)
    return f[freq_mask], t, Sxx_norm[freq_mask, :]


# === MULTI-CHANNEL PLOTTER ===
def plot_and_save_spectrograms(data, fs, filename):
    n_channels = data.shape[1] if data.ndim > 1 else 1
    fig, axes = plt.subplots(n_channels, 1, figsize=(10, 3.5 * n_channels), sharex=True)

    if n_channels == 1:
        axes = [axes]

    for ch in range(n_channels):
        signal_data = data[:, ch] if n_channels > 1 else data
        f, t, Sxx_filtered = compute_normalized_spectrogram(signal_data, fs)

        im = axes[ch].pcolormesh(t, f, 10 * np.log10(Sxx_filtered + 1e-12),
                                 shading='gouraud', cmap='viridis')
        axes[ch].set_ylabel("Freq [Hz]")
        axes[ch].set_title(f"Channel {ch + 1}")
        fig.colorbar(im, ax=axes[ch], orientation='vertical', label='Normalized Power (dB)')

    axes[-1].set_xlabel("Time [s]")
    fig.suptitle(f"Normalized 1–2 Hz Spectrograms — {filename}", fontsize=14)
    fig.tight_layout(rect=[0, 0, 1, 0.95])

    out_path = os.path.join(output_folder, f"{os.path.splitext(filename)[0]}_spectrogram_1to2Hz_cpu.png")
    plt.savefig(out_path, dpi=150)
    plt.close()
    print(f"✅ Saved spectrogram plot: {out_path}")


# === MAIN LOOP (PARALLELIZED) ===
if __name__ == "__main__":
    dat_files = [f for f in os.listdir(input_folder) if f.endswith(".dat")]

    if not dat_files:
        print(f"No .dat files found in '{input_folder}'.")
    else:
        print(f"🔧 Found {len(dat_files)} files. Processing in parallel on CPU cores...")

        def process_file(file):
            path = os.path.join(input_folder, file)
            print(f"\nProcessing {file}...")
            data, fs = read_dat_file(path)
            if data.ndim == 1:
                data = data.reshape(-1, 1)
            data = normalize_signal_numba(data)
            plot_and_save_spectrograms(data, fs, file)

        # Use all CPU cores
        Parallel(n_jobs=-1, backend="loky")(delayed(process_file)(file) for file in dat_files)
