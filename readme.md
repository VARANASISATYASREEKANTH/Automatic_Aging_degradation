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

Researchers can extract **time–frequency features** (e.g., LF/HF ratios, entropy, spectral power) from these spectrograms to model **“autonomic age”** or detect **early signs of dysautonomia**.

---

## ⚙️ Spectrogram Generation Script

This repository includes a Python script:

```bash
spectrogram_plot.py
