# fetch_data.py
import requests
import pandas as pd
from io import StringIO

def download_nasa_data():
    print("Querying NASA Exoplanet Archive API...")
    
    # Astronomical Data Query Language (ADQL) query
    # Pulling: name, star name, method, year, radius (Earths), mass (Earths), orbit (days), star temp (K), distance (parsecs)
    query = """
    select pl_name, hostname, discoverymethod, disc_year, 
           pl_rade, pl_masse, pl_orbper, st_teff, sy_dist 
    from pscomppars
    """
    
    # Format the URL for the TAP API
    url = f"https://exoplanetarchive.ipac.caltech.edu/TAP/sync?query={query}&format=csv"
    
    response = requests.get(url)
    response.raise_for_status()
    
    # Load into pandas to drop empty rows (cleaning the dataset)
    df = pd.read_csv(StringIO(response.text))
    df = df.dropna(subset=['pl_rade', 'pl_masse', 'st_teff'])
    
    # Save locally
    output_path = "data/exoplanets.csv"
    df.to_csv(output_path, index=False)
    print(f"Success! Downloaded {len(df)} confirmed exoplanets with complete physical profiles to {output_path}.")

if __name__ == "__main__":
    download_nasa_data()