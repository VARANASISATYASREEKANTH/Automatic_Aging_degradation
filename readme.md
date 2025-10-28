# 🧠 Spectrogram Analysis of the Automatic Aging Dataset (PhysioNet)

This repository demonstrates how to read, normalize, and visualize **spectrograms** from the [Automatic Aging of the Autonomic Nervous System Dataset](https://physionet.org/content/autonomic-aging-cardiovascular/1.0.0/), available on PhysioNet.  

The spectrograms reveal **autonomic nervous system (ANS)** activity patterns across aging populations, showing how **cardiovascular and respiratory regulation** changes with age.

---

## 📘 Dataset Overview

The **Automatic Aging Dataset** contains physiological recordings such as:

- 🫀 **ECG (Electrocardiogram)** – cardiac electrical activity  
- 💓 **PPG (Photoplethysmogram)** – blood volume pulse  
- 🌬 **RESP (Respiration)** – breathing signal  
- 💢 **BP (Blood Pressure)** – arterial pressure waveform  
- ⚡ **EDA (Electrodermal Activity)** – skin conductance (sympathetic response)  

Each subject underwent standardized **autonomic function tests**, including:

- Deep breathing test  
- Valsalva maneuver  
- Head-up tilt  
- Cold pressor test  
- Orthostatic challenge  

These tests evoke **sympathetic** and **parasympathetic** nervous system activity, allowing analysis of aging effects on autonomic balance.

---

## 🎛 What the Spectrogram Represents

A **spectrogram** is a time–frequency representation of a signal, showing how energy is distributed over time and frequency.

| Axis | Represents |
|------|-------------|
| **X-axis** | Time (seconds) |
| **Y-axis** | Frequency (Hz) |
| **Color** | Signal power or energy (dB/Hz) |

---

## ❤️ Interpreting Spectrograms by Signal Type

### **1. ECG Spectrogram**
- Dominant frequency ≈ **1–2 Hz** (60–120 beats per minute).
- Harmonics arise from sharp QRS complexes.
- **Younger subjects:** strong low- and high-frequency variability (heart rate variability).
- **Older subjects:** narrow, more constant band — reduced HRV and vagal modulation.

### **2. PPG Spectrogram**
- Primary frequency near **1 Hz** (pulse rate).
- Power fluctuations represent **vascular tone modulation**.
- **Aging:** smoother, more uniform spectrum → decreased vasomotor flexibility.

### **3. Respiration Spectrogram**
- Dominant band ≈ **0.2–0.3 Hz** (12–18 breaths/min).
- Shows clear rhythm changes during controlled breathing.
- **Aging:** reduced amplitude and frequency variation, weaker coupling to HR.

### **4. BP and EDA Spectrograms**
- Low-frequency (<0.1 Hz) oscillations correspond to **Mayer waves** and **sympathetic activation**.
- **Younger:** dynamic LF modulation.
- **Older:** flattened spectra → reduced baroreflex and sympathetic adaptability.

---

## 📊 Spectrogram Changes with Aging

| Spectral Feature | Younger Subjects | Older Subjects |
|------------------|------------------|----------------|
| Heart Rate Variability | Strong LF/HF power (broad spectrum) | Narrow, reduced spectral power |
| Respiratory Coupling | Clear 0.25 Hz ridge | Weak or absent |
| PPG Variability | High amplitude modulation | Minimal variation |
| EDA Response | Distinct bursts | Weak or absent |
| LF/HF Ratio | Balanced sympathetic–parasympathetic | Shifted toward sympathetic |

> 🧩 **Interpretation:**  
> Aging reduces the *dynamic range* of autonomic regulation — visible as smoother, narrower, and less time-varying spectrograms across all physiological channels.

---

## 🔬 Scientific Insight

Spectrogram analysis provides a visual and quantitative way to observe **autonomic decline** with age:
- Decreased **HRV (Heart Rate Variability)**  
- Weakened **respiratory sinus arrhythmia**  
- Reduced **baroreflex sensitivity**  
- Lower **sympathetic reactivity**

# 🩺 ECG Spectrogram Anomaly Detection

This repository explains how **spectrograms of ECG (Electrocardiogram) signals** can be used to **detect cardiac anomalies**.  
By converting ECG waveforms into time–frequency representations, we can visually and algorithmically detect abnormal patterns related to heart rhythm and morphology.

---
## ⚙️ ECG Frequency Components Reference

| **ECG Component**  | **Typical Frequency Range (Hz)** |
| ------------------ | -------------------------------- |
| P wave             | 0.5 – 10                         |
| QRS complex        | 8 – 50                           |
| T wave             | 1 – 7                            |
| Muscle noise / EMG | > 50                             |
| Baseline drift     | < 0.5                            |

## 🔍 1. What Is a Spectrogram?

A **spectrogram** is a time–frequency representation of a signal.

- **X-axis:** Time (seconds)
- **Y-axis:** Frequency (Hz)
- **Color intensity:** Power (amplitude) of frequency components

In ECG, most of the signal energy lies below **50 Hz**.  
Spectrograms reveal how these frequencies change over time — which is highly useful for detecting anomalies.

---

## 💓 2. Normal ECG Spectrogram

- Shows **periodic, low-frequency bursts** corresponding to the **P–QRS–T** complex.
- Dominant frequency band: **0.5 – 40 Hz**.
- Energy distribution is **cyclic and stable** across time.

---

## ⚠️ 3. Common ECG Anomalies Detectable via Spectrogram

| **Anomaly Type** | **Spectrogram Features / Patterns** | **Physiological Meaning** |
|------------------|-------------------------------------|----------------------------|
| **Arrhythmia** | Non-periodic energy bursts; irregular spacing of QRS-related energy | Irregular heartbeat pattern |
| **Atrial Fibrillation (AF)** | Continuous low-frequency energy (3–8 Hz) without periodic structure | Chaotic atrial activity |
| **Ventricular Tachycardia (VT)** | Broad repetitive high-energy bands; reduced variability | Rapid ventricular rhythm |
| **Bradycardia** | Long intervals between bursts | Slow heart rate |
| **Tachycardia** | Closely spaced bursts; slightly higher power | Fast heart rate |
| **Myocardial Ischemia (MI)** | Reduced energy in mid-frequency bands; altered QRS–T patterns | Damaged heart muscle conduction |
| **Bundle Branch Block (LBBB/RBBB)** | Broadened QRS energy regions | Delayed ventricular conduction |
| **Premature Ventricular Contraction (PVC)** | Isolated, high-energy spikes disrupting regular rhythm | Early abnormal beats |
| **Noise / Muscle Artifact** | High-frequency (>40 Hz) random activity | EMG or motion interference |
| **Baseline Wander** | Low-frequency (<0.5 Hz) oscillations | Electrode movement or breathing artifact |

---

## 🧠 4. Detection Approaches

### (a) Manual / Visual Inspection
- Experts can spot irregular periodicity, color changes, or abrupt frequency shifts in spectrograms.

### (b) Automated Machine Learning Methods
1. **Convolutional Neural Networks (CNNs):**  
   Treat spectrograms as 2D images for classification (AF, PVC, etc.).
2. **Autoencoders / VAEs:**  
   Learn normal spectrograms and detect anomalies by reconstruction error.
3. **Transformers (ViT):**  
   Capture long-term temporal and spectral dependencies.
4. **Statistical Features:**  
   Metrics like spectral entropy, variance, and dominant frequency help detect irregularities.

---
## 📘 References

1. **Goldberger, A. L., et al. (2000).**  
   *PhysioBank, PhysioToolkit, and PhysioNet: Components of a New Research Resource for Complex Physiologic Signals.*  
   _Circulation_, 101(23), e215–e220.  
   [https://physionet.org](https://physionet.org)

2. **Moody, G. B., & Mark, R. G. (2001).**  
   *The impact of the MIT-BIH Arrhythmia Database.*  
   _IEEE Engineering in Medicine and Biology Magazine_, 20(3), 45–50.  
   [DOI:10.1109/51.932724](https://doi.org/10.1109/51.932724)

3. **Acharya, U. R., et al. (2017).**  
   *A deep convolutional neural network model to classify heartbeats.*  
   _Computers in Biology and Medicine_, 89, 389–396.  
   [DOI:10.1016/j.compbiomed.2017.08.022](https://doi.org/10.1016/j.compbiomed.2017.08.022)

4. **Minami, K., Nakajima, H., & Toyoshima, T. (1999).**  
   *Real-time discrimination of ventricular tachyarrhythmia with Fourier-transform neural network.*  
   _IEEE Transactions on Biomedical Engineering_, 46(2), 179–185.  
   [DOI:10.1109/10.740875](https://doi.org/10.1109/10.740875)

5. **Zhang, Z., et al. (2019).**  
   *Heart sound classification using deep learning and time–frequency features.*  
   _IEEE Access_, 7, 119857–119865.  
   [DOI:10.1109/ACCESS.2019.2936014](https://doi.org/10.1109/ACCESS.2019.2936014)

6. **Li, D., et al. (2020).**  
   *Atrial fibrillation detection using spectrogram-based convolutional neural network.*  
   _Frontiers in Physiology_, 11, 593.  
   [DOI:10.3389/fphys.2020.00593](https://doi.org/10.3389/fphys.2020.00593)

7. **Martis, R. J., Acharya, U. R., & Lim, C. M. (2013).**  
   *ECG beat classification using PCA, LDA, ICA and discrete wavelet transform.*  
   _Biomedical Signal Processing and Control_, 8(5), 437–448.  
   [DOI:10.1016/j.bspc.2013.01.005](https://doi.org/10.1016/j.bspc.2013.01.005)

8. **Oweis, R. J., & Abdulhay, E. (2011).**  
   *Separation of cardiac and noise components from ECG signals by adaptive filtering and spectral analysis.*  
   _Computers in Biology and Medicine_, 41(5), 432–441.  
   [DOI:10.1016/j.compbiomed.2011.03.001](https://doi.org/10.1016/j.compbiomed.2011.03.001)

9. **Clifford, G. D., et al. (2017).**  
   *AF classification from a short single lead ECG recording: The PhysioNet Computing in Cardiology Challenge 2017.*  
   _Computing in Cardiology Conference_, 44, 1–4.  
   [https://physionet.org/challenge/2017/](https://physionet.org/challenge/2017/)

10. **Rajpurkar, P., et al. (2017).**  
    *Cardiologist-level arrhythmia detection with convolutional neural networks.*  
    _Nature Medicine_, 25, 65–69.  
    [DOI:10.1038/s41591-018-0268-3](https://doi.org/10.1038/s41591-018-0268-3)

## 📊 5. Example Analysis Flow

```python
import numpy as np
from scipy import signal
import matplotlib.pyplot as plt

# Example ECG signal and sampling rate
fs = 1000  # Hz
ecg_signal = np.load('ecg_sample.npy')

# Compute spectrogram
frequencies, times, Sxx = signal.spectrogram(ecg_signal, fs=fs)

# Plot
plt.figure(figsize=(10, 4))
plt.pcolormesh(times, frequencies, 10 * np.log10(Sxx))
plt.ylabel('Frequency [Hz]')
plt.xlabel('Time [s]')
plt.title('ECG Spectrogram')
plt.colorbar(label='Power (dB)')
plt.show()
