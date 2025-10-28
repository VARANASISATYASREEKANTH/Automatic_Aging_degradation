# -*- coding: utf-8 -*-
"""
Created on Mon Oct 27 19:13:18 2025

@author: SREEKANTHVS
"""


import os
import numpy as np
import matplotlib.pyplot as plt

# Try to import GPU version (CuPy)
try:
    import cupy as cp
    GPU_AVAILABLE = True
    print("✅ CuPy GPU acceleration enabled.")
except ImportError:
    cp = np
    GPU_AVAILABLE = False
    print("⚠️ CuPy not found — running on CPU. Install with 'pip install cupy-cuda12x'")

# Try to import wfdb for PhysioNet .dat files
try:
    import wfdb
    USE_WFDB = True
except ImportError:
    USE_WFDB = False
    print("⚠️ wfdb not found. Install with 'pip install wfdb' if using PhysioNet .dat files.")

# === CONFIG ===
input_folder = r"C:\research_work_DIMAAG_AI_SSE\work_progress_reports\work_report_2025_2026\my_projects\AUTOMATIC_AGING\DATASETS\AA_DATASETS"
output_folder = r"C:\research_work_DIMAAG_AI_SSE\work_progress_reports\work_report_2025_2026\my_projects\AUTOMATIC_AGING\RESULTS\gpu_filtered_spectrograms"
default_fs = 1000  # Hz

os.makedirs(output_folder, exist_ok=True)

# === READ FUNCTION ===
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

    # Fallback
    try:
        data = np.loadtxt(filepath)
        fs = default_fs
    except Exception:
        data = np.fromfile(filepath, dtype=np.float32)
        fs = default_fs

    print(f"  -> Loaded {data.shape[0]} samples (fallback mode), fs={fs} Hz")
    return data, fs


# === NORMALIZATION ===
def normalize_signal(data):
    """Normalize to zero mean, unit variance."""
    xp = cp if GPU_AVAILABLE else np
    data_gpu = xp.asarray(data)
    mean = xp.mean(data_gpu, axis=0)
    std = xp.std(data_gpu, axis=0) + 1e-8
    data_gpu = (data_gpu - mean) / std
    return cp.asnumpy(data_gpu) if GPU_AVAILABLE else data_gpu


# === GPU Spectrogram ===
def compute_spectrogram_gpu(signal_data, fs=1000, nperseg=1024):
    """
    Compute spectrogram using GPU FFT.
    Equivalent to scipy.signal.spectrogram but using CuPy FFT.
    """
    xp = cp if GPU_AVAILABLE else np

    # Windowing
    step = nperseg // 2
    n_frames = (len(signal_data) - nperseg) // step + 1
    freqs = xp.fft.rfftfreq(nperseg, d=1 / fs)

    # Create 2D array of windowed segments
    frames = xp.lib.stride_tricks.sliding_window_view(signal_data, nperseg)[::step]
    window = xp.hanning(nperseg)

    # FFT on GPU
    fft_frames = xp.fft.rfft(frames * window, axis=1)
    Sxx = xp.abs(fft_frames) ** 2 / (fs * xp.sum(window ** 2))

    # Normalize PSD
    Sxx_sum = xp.sum(Sxx, axis=0, keepdims=True) + 1e-12
    Sxx_norm = Sxx / Sxx_sum

    # Back to CPU for plotting
    return np.asarray(freqs), np.linspace(0, len(signal_data)/fs, n_frames), np.asarray(Sxx_norm)


# === PLOT & SAVE ===
def plot_and_save_spectrograms(data, fs, filename):
    n_channels = data.shape[1] if data.ndim > 1 else 1
    fig, axes = plt.subplots(n_channels, 1, figsize=(10, 4 * n_channels), sharex=True)
    if n_channels == 1:
        axes = [axes]

    for ch in range(n_channels):
        signal_data = data[:, ch] if n_channels > 1 else data
        f, t, Sxx_norm = compute_spectrogram_gpu(signal_data, fs=fs, nperseg=1024)

        im = axes[ch].pcolormesh(t, f, 10 * np.log10(Sxx_norm + 1e-12),
                                 shading='gouraud', cmap='inferno')
        axes[ch].set_ylabel("Freq [Hz]")
        axes[ch].set_title(f"Channel {ch + 1}")
        fig.colorbar(im, ax=axes[ch], orientation='vertical', label='Power (dB)')

    axes[-1].set_xlabel("Time [s]")
    fig.suptitle(f"Spectrograms (GPU Accelerated) — {filename}", fontsize=14)
    fig.tight_layout(rect=[0, 0, 1, 0.96])

    out_path = os.path.join(output_folder, f"{os.path.splitext(filename)[0]}_spectrogram_gpu.png")
    plt.savefig(out_path, dpi=150)
    plt.close()
    print(f"✅ Saved GPU spectrogram plot: {out_path}")


# === MAIN ===
if __name__ == "__main__":
    dat_files = [f for f in os.listdir(input_folder) if f.endswith(".dat")]
    if not dat_files:
        print(f"No .dat files found in '{input_folder}'.")
    else:
        for file in dat_files:
            print(f"\nProcessing {file}...")
            path = os.path.join(input_folder, file)
            data, fs = read_dat_file(path)
            data = normalize_signal(data)
            plot_and_save_spectrograms(data, fs, file)
