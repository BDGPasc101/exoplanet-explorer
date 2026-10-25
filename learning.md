# NASA Exoplanet Dashboard - Project Learnings

## 1. Web UI & Framework (Streamlit)
* **Why we used Streamlit:** It translates Python scripts directly into a modern React.js web interface. This allows Research Software Engineers to build interactive tools without writing any HTML/CSS/JS.
* **App Performance (`@st.cache_data`):** We used this decorator above our data-loading function. 
  * *Why:* Streamlit reruns the entire script every time a user clicks a button or moves a slider. Caching forces the app to load the dataset into memory only once, keeping the dashboard lightning fast.
* **Stateful UI Design:** Initially tried to make the 3D Plotly graph clickable, but Plotly's 3D engine doesn't support click-events well.
  * *The Fix:* Built a searchable dropdown menu tied to the Pandas dataframe state. 
  * *Why:* It's a much better User Experience (UX) and bypasses third-party library limitations.

## 2. Data Engineering & Environment
* **Virtual Environments (`venv`):** Created an isolated Python environment for this project.
  * *Why:* Prevents dependency conflicts with other projects (like the Ising Model) and ensures we know exactly which packages to put in our `requirements.txt` for cloud deployment.
* **Automated Data Ingestion (API):** Instead of manually downloading a CSV from NASA, we wrote a Python script (`fetch_data.py`) to query NASA's TAP API using ADQL (Astronomical Data Query Language).
  * *Why:* It makes the data pipeline automated, reproducible, and easy to update with new planetary discoveries.

## 3. Feature Engineering & Astrophysics 
* **Stellar Stability Toggle:** Added a filter for Stellar Effective Temperature ($T_{eff}$) between 2,500 K and 6,000 K.
  * *Why:* This specifically isolates M, K, and G-type main-sequence stars (stable, long-lived stars).
* **Distance Filter:** Added a slider to filter by distance from our solar system (in parsecs) to focus on locally observable candidates.
* **Filtering Volatile Stars:** Updated the API fetch to pull star age (`st_age`).
  * *Why:* We noticed planets like AU Mic d showing up as "Earth-like," but it orbits an infant star that emits sterilizing radiation spikes. Filtering out stars < 1 Billion years old fixed this false positive.
* **Habitable Zone (HZ) Math:** Engineered new columns to calculate conservative liquid water boundaries. 
  * *Why:* We used the Stefan-Boltzmann law to estimate star luminosity, then calculated the inner and outer HZ boundaries in AU to see if a planet's orbit actually fell in the "Goldilocks" zone.

## 4. The Earth Similarity Index (ESI)
Built a custom ESI score using Pandas mathematical functions. The standard ESI uses a mathematical concept called a distance metric. Because our dataset measures mass and radius in "Earth units" (meaning Earth = $1.0$), we can calculate the similarity for any property $x$ using this formula:

$$ \text{Similarity} = 1 - \left| \frac{x - 1}{x + 1} \right| $$

If a planet's mass is exactly 1, the result is $1.0$ (perfect match). If it is vastly larger or smaller, it approaches $0.0$. We calculated this for both mass and radius, and multiplied them together for our final ESI score (visualized as a progress bar).

## 5. Results & Deployment
* **The Final Cut:** Out of over 5,000 confirmed exoplanets, applying strict astrophysical filters (rocky mass, stable/mature star, and conservative habitable zone) left only 2 prime candidates: **TRAPPIST-1 e** and **GJ 1061 d**. 
* **Cloud Deployment:** We pushed the code to GitHub and linked it to Streamlit Community Cloud using our `requirements.txt`.
  * *Why:* Moves the project from a local script to a live, public web app that can be shared on a resume.

## 6. Future Ideas to Explore
* Integrate my study of galactic metallicity regions from my undergrad dissertation to filter stars based on their galactic environment and composition.