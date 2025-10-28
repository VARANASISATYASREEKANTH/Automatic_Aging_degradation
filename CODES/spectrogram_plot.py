import os
import numpy as np
import matplotlib.pyplot as plt
from scipy import signal

# Try to import wfdb for PhysioNet .dat files
try:
    import wfdb
    USE_WFDB = True
except ImportError:
    USE_WFDB = False
    print("⚠️ wfdb not found. Install with 'pip install wfdb' if using PhysioNet .dat files.")

# === CONFIG ===
input_folder = "C:/research_work_DIMAAG_AI_SSE/work_progress_reports/work_report_2025_2026/my_projects/AUTOMATIC_AGING/DATASETS/AA_DATASETS"       # Folder containing .dat and .hea files
output_folder = "C:/research_work_DIMAAG_AI_SSE/work_progress_reports/work_report_2025_2026/my_projects/AUTOMATIC_AGING/RESULTS/filtered_spectrograms"  # Folder to save spectrogram plots
default_fs = 1000                     # Default sampling rate if not found in header

# === CREATE OUTPUT FOLDER ===
os.makedirs(output_folder, exist_ok=True)

# === FUNCTION TO READ .DAT FILE ===
def read_dat_file(filepath):
    """Reads PhysioNet .dat + .hea files using wfdb if available, else raw numeric/binary."""
    base = os.path.splitext(filepath)[0]

    if USE_WFDB and os.path.exists(base + '.hea'):
        try:
            record = wfdb.rdrecord(base)
            data = record.p_signal
            fs = record.fs
            print(f"  -> Loaded {data.shape[0]} samples, {data.shape[1]} channels, fs={fs} Hz")
            return data, fs
        except Exception as e:
            print(f"⚠️ WFDB failed to read {filepath}: {e}")

    # Fallback for non-PhysioNet files
    try:
        data = np.loadtxt(filepath)
        fs = default_fs
    except Exception:
        data = np.fromfile(filepath, dtype=np.float32)
        fs = default_fs

    print(f"  -> Loaded {data.shape[0]} samples (fallback mode), fs={fs} Hz")
    return data, fs

# === FUNCTION TO NORMALIZE DATA ===
def normalize_signal(data):
    """Normalize each channel to zero mean and unit variance."""
    if data.ndim == 1:
        return (data - np.mean(data)) / (np.std(data) + 1e-8)
    else:
        norm_data = np.zeros_like(data)
        for ch in range(data.shape[1]):
            norm_data[:, ch] = (data[:, ch] - np.mean(data[:, ch])) / (np.std(data[:, ch]) + 1e-8)
        return norm_data

# === FUNCTION TO PLOT MULTI-CHANNEL SPECTROGRAM ===
def plot_and_save_spectrograms(data, fs, filename):
    """Plots each channel’s spectrogram as a separate subplot."""
    n_channels = data.shape[1] if data.ndim > 1 else 1
    fig, axes = plt.subplots(n_channels, 1, figsize=(10, 4 * n_channels), sharex=True)

    if n_channels == 1:
        axes = [axes]  # Make iterable for single channel

    for ch in range(n_channels):
        signal_data = data[:, ch] if n_channels > 1 else data
        f, t, Sxx = signal.spectrogram(signal_data, fs=1000, nperseg=1024)
        Sxx_sum = np.sum(Sxx, axis=0, keepdims=True)
        Sxx_norm = Sxx / (Sxx_sum + 1e-12)
        im = axes[ch].pcolormesh(t, f, 10 * np.log10(Sxx_norm + 1e-12), shading='gouraud',cmap='hsv')
        axes[ch].set_ylabel('Freq [Hz]')
        axes[ch].set_title(f'Channel {ch + 1}')
        fig.colorbar(im, ax=axes[ch], orientation='vertical', label='Power/Frequency (dB/Hz)')

    axes[-1].set_xlabel('Time [sec]')
    fig.suptitle(f"Spectrograms - {filename}", fontsize=14)
    fig.tight_layout(rect=[0, 0, 1, 0.96])

    out_path = os.path.join(output_folder, f"{os.path.splitext(filename)[0]}_spectrogram.png")
    plt.savefig(out_path, dpi=100)
    plt.close()
    print(f"✅ Saved spectrogram plot: {out_path}")

# === MAIN LOOP ===
if __name__ == "__main__":
    dat_files = [f for f in os.listdir(input_folder) if f.endswith('.dat')]

    if not dat_files:
        print(f"No .dat files found in '{input_folder}'.")
    else:
        for file in dat_files[1051:1121]:
            path = os.path.join(input_folder, file)
            print(f"\nProcessing {file}...")
            data, fs = read_dat_file(path)
            data = normalize_signal(data)
            plot_and_save_spectrograms(data, fs, file)
