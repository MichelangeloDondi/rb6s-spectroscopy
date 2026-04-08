# rb6s-spectroscopy

[![Python 3.9+](https://img.shields.io/badge/python-3.9+-blue.svg)](https://www.python.org/downloads/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)

**High-Precision Two-Photon Spectroscopy Fitting Pipeline for Rubidium 6S State.**

This repository contains a specialized data analysis pipeline designed to extract precise collisional broadening rates ($\Gamma_L$) for the Rubidium $5S_{1/2} \to 6S_{1/2}$ two-photon transition at **993 nm** in thermal vapor cells.

By leveraging an **Electro-Optic Modulator (EOM)** for absolute frequency calibration and a **Bottom-Up nested fitting architecture**, this pipeline eliminates systemic errors from laser non-linearities and rigorously accounts for experimental imperfections such as Residual Amplitude Modulation (RAM).

---

# 🔬 Methodology

# 1. Dynamic EOM Comb Calibration
Piezo-driven scans are inherently non-linear. This pipeline uses the EOM sidebands as a "frequency ruler," calibrating the X-axis against a stable RF oscillator rather than relying on time or voltage linearity.

# 2. RAM Asymmetry Handling
Polarization mismatches entering the EOM crystal can generate asymmetric sidebands (Residual Amplitude Modulation). The `eom_asymmetric_comb` model assigns independent amplitude parameters to left/right sidebands, preventing the algorithm from artificially skewing the Lorentzian linewidth to compensate for amplitude imbalances.

# 3. Bottom-Up Nested Fitting
To avoid local minima and overfitting, we implement a multi-stage fitting strategy:
* **Stage 1 (3-Peak):** Locks fundamental parameters (Center, $\Gamma_L$, $\sigma_G$) using the carrier and 1st order sidebands.
* **Stage 2 & 3 (5/7-Peak):** Progressively adds higher-order sidebands using previous results as high-confidence initial guesses, validated by the **Bayesian Information Criterion (BIC)**.

# 4. Zero-Power Extrapolation
Analyzes a power series to eliminate **AC Stark shifts** and **differential power broadening**, isolating the pure homogeneous linewidth (natural + collisional).

---

## 📂 Project Structure
```text
rb_twophoton_fit/
├── README.md               # You are here
├── requirements.txt        # Python dependencies
├── config/
│   ├── eom_calibration.yaml  # Hardware and RF parameters
│   ├── physics.yaml          # Atomic constants and transitions
│   └── fitting.yaml          # Optimization tolerances and models
├── data/                   
│   ├── 01_raw/             # Immutable oscilloscope traces (Not tracked by Git)
│   ├── 02_interim/         # Frequency-calibrated X-axis arrays (.npz)
│   └── 03_processed/       # Final parameters and extracted linewidths
├── figures/                # Publication-ready plots
├── src/                    # Core Physics & Mathematics Engine
│   ├── config_loader.py    # YAML parser
│   ├── data_processor.py   # Statistical weighting and Axis calibration
│   ├── models.py           # Faddeeva Voigt profiles & Asymmetric Comb
│   └── fitter.py           # lmfit objective functions & param builders
└── notebooks/              # Executable Pipeline
    ├── 01_eom_nested_fit.ipynb         # Calibration & Bottom-Up extraction
    ├── 02_global_power_analysis.ipynb  # Power series fitting
    └── 03_zero_power_extrap.ipynb      # Asymptotic zero-power limit

---

## 🚀 Quick Start

### 1. Environment Setup
```bash
# Clone and enter the repository
git clone [https://github.com/MichelangeloDondi/rb6s-spectroscopy.git](https://github.com/MichelangeloDondi/rb6s-spectroscopy.git)
cd rb6s-spectroscopy

# Create and activate virtual environment
python3 -m venv venv
source venv/bin/activate

# Install dependencies
pip install -r requirements.txt

--------------------------------------------------------------------------------

Developed for research at the Okinawa Institute of Science and Technology (OIST).