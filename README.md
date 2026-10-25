# 🌌 NASA Exoplanet Habitability Explorer

> **Live Demo:** [View the Interactive Dashboard on Streamlit Cloud](https://exoplanet-explorer-ykjq8potsenmhvmou2awrv.streamlit.app/)

An interactive, web-based data exploration tool built to filter, analyze, and visualize over 5,000 confirmed exoplanets from the NASA Exoplanet Archive. This dashboard acts as a decision-support tool, allowing researchers to cut through raw astronomical data to identify potentially habitable, Earth-like candidates using programmatic astrophysical modeling.

## 🚀 Key Features

* **Automated Data Ingestion:** Connects directly to NASA's Table Access Protocol (TAP) API via Astronomical Data Query Language (ADQL) to fetch and clean the latest planetary systems data.
* **Interactive 3D Visualization:** Maps exoplanets across orbital period, mass, and radius using a fully interactive Plotly 3D scatter plot, color-coded by host star temperature.
* **Algorithmic Habitability Filtering:** 
  * Isolates mature, stable main-sequence stars (2,500K - 6,000K, >1 Gyr).
  * Calculates conservative Habitable Zone (HZ) boundaries using stellar luminosity and the Stefan-Boltzmann law.
  * Filters for terrestrial mass (0.5-5.0 M⊕) and radius (0.8-1.6 R⊕).
* **Earth Similarity Index (ESI) Engineering:** Synthesizes raw mass and radius parameters into a normalized 0.0-1.0 similarity score to rank planetary physical characteristics against Earth.
* **Stateful UI Design:** Features dynamic dropdowns and real-time profile rendering tied to Pandas dataframe states, bypassing 3D web-GL event limitations.

## 🛠️ Tech Stack

* **Frontend & Web Server:** Streamlit
* **Data Processing & Feature Engineering:** Pandas, NumPy
* **3D Rendering:** Plotly Express
* **Data Source:** NASA Exoplanet Archive (Caltech/IPAC) API

## 💻 Local Installation

To run this dashboard on your local machine:

1. **Clone the repository:**
   ```bash
   git clone https://github.com/BDGPasc101/exoplanet-explorer.git
   cd exoplanet-explorer
   ```

2. **Create a virtual environment and install dependencies:**
   ```bash
   python3 -m venv venv
   source venv/bin/activate  # On Windows: .\venv\Scripts\activate
   pip install -r requirements.txt
   ```

3. **Fetch the latest NASA dataset:**
   ```bash
   python fetch_data.py
   ```

4. **Launch the Streamlit app:**
   ```bash
   streamlit run app.py
   ```

## 🧠 Scientific Methodology

The logic powering the "Habitable Zone" and "Earth-Like" filters relies on conservative astrophysical constraints:
1. **Stellar Stability:** Excludes O, B, A, and F-type stars due to extreme UV/X-ray emissions and short lifespans, focusing on G, K, and M-dwarfs. Infant stars (< 1 Gyr) are filtered out to avoid early-stage stellar volatility.
2. **Habitable Zone (HZ):** Stellar luminosity is estimated relative to the Sun ($L_{\odot} = 1$). Conservative inner and outer boundaries are calculated in Astronomical Units (AU) to determine the region where liquid water could theoretically pool on a rocky surface.

---
*Developed as a portfolio project demonstrating Research Software Engineering, full-stack data pipelines, and domain-specific feature engineering.*