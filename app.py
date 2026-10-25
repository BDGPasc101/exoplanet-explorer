import streamlit as st
import pandas as pd
import plotly.express as px

st.set_page_config(page_title="Exoplanet Explorer", layout="wide")

@st.cache_data
def load_data():
    return pd.read_csv("data/exoplanets.csv")

st.title("?? NASA Exoplanet Habitability Explorer")
st.markdown("Filter and visualize thousands of confirmed exoplanets to identify potential Earth-like candidates.")

df = load_data()

# --- SIDEBAR FILTERS ---
st.sidebar.header("Filter Parameters")

# Filter by Mass (Earth Masses)
max_mass = float(df['pl_masse'].max())
mass_range = st.sidebar.slider(
    "Planetary Mass (Earth Masses)", 
    0.0, 50.0, (0.0, 20.0) # Default to looking for smaller, rocky planets
)

# Filter by Star Temperature (Kelvin)
temp_range = st.sidebar.slider(
    "Host Star Temperature (K)", 
    2000, 10000, (2000, 7000) # Our sun is ~5778K
)

# Apply filters
filtered_df = df[
    (df['pl_masse'] >= mass_range[0]) & (df['pl_masse'] <= mass_range[1]) &
    (df['st_teff'] >= temp_range[0]) & (df['st_teff'] <= temp_range[1])
]

# --- METRICS ---
col1, col2 = st.columns(2)
col1.metric(label="Total Confirmed Planets", value=f"{len(df):,}")
col2.metric(label="Planets Matching Criteria", value=f"{len(filtered_df):,}")

# --- 3D VISUALIZATION ---
st.subheader("3D Exoplanet Distribution")

if not filtered_df.empty:
    fig = px.scatter_3d(
        filtered_df, 
        x='pl_orbper', 
        y='pl_masse', 
        z='pl_rade',
        color='st_teff',
        color_continuous_scale='plasma',
        hover_name='pl_name',
        hover_data={'discoverymethod': True, 'sy_dist': True},
        labels={
            'pl_orbper': 'Orbital Period (Days)',
            'pl_masse': 'Mass (Earths)',
            'pl_rade': 'Radius (Earths)',
            'st_teff': 'Star Temp (K)'
        }
    )
    
    # Adjust layout for better viewing
    fig.update_layout(scene=dict(
        xaxis_type="log", # Log scale because orbits range from days to centuries
        yaxis_type="log"
    ), margin=dict(l=0, r=0, b=0, t=0), height=600)
    
    st.plotly_chart(fig, use_container_width=True)
else:
    st.warning("No planets match your current filter criteria.")

# --- DATA TABLE ---
st.subheader("Filtered Dataset")
st.dataframe(filtered_df)