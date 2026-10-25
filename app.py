import streamlit as st
import pandas as pd
import plotly.express as px
import urllib.parse

st.set_page_config(page_title="Exoplanet Explorer", layout="wide")

@st.cache_data
def load_data():
    df = pd.read_csv("data/exoplanets.csv")
    
    # Map temperature to standard stellar classifications
    def classify_star(temp):
        if pd.isna(temp): return "Unknown"
        if temp >= 30000: return "O-Type (Blue)"
        elif temp >= 10000: return "B-Type (Blue-White)"
        elif temp >= 7500: return "A-Type (White)"
        elif temp >= 6000: return "F-Type (Yellow-White)"
        elif temp >= 5200: return "G-Type (Yellow, Sun-like)"
        elif temp >= 3700: return "K-Type (Orange Dwarf)"
        else: return "M-Type (Red Dwarf)"
        
    df['Star Class'] = df['st_teff'].apply(classify_star)
    
    # --- NEW: Feature Engineering the ESI ---
    # Calculate similarity for Radius and Mass
    esi_radius = 1 - abs((df['pl_rade'] - 1) / (df['pl_rade'] + 1))
    esi_mass = 1 - abs((df['pl_masse'] - 1) / (df['pl_masse'] + 1))
    
    # Combine for final ESI score (0.0 to 1.0)
    df['ESI'] = esi_radius * esi_mass
    # --- Feature Engineering the ESI ---
    esi_radius = 1 - abs((df['pl_rade'] - 1) / (df['pl_rade'] + 1))
    esi_mass = 1 - abs((df['pl_masse'] - 1) / (df['pl_masse'] + 1))
    df['ESI'] = esi_radius * esi_mass
    
    # --- NEW: Habitable Zone Math ---
    # 1. Estimate Star Luminosity relative to our Sun (L_sun = 1)
    df['st_lum_est'] = (df['st_rad'] ** 2) * ((df['st_teff'] / 5778) ** 4)
    
    # 2. Calculate conservative inner and outer boundaries (in AU)
    df['hz_inner'] = (df['st_lum_est'] / 1.1) ** 0.5
    df['hz_outer'] = (df['st_lum_est'] / 0.53) ** 0.5
    
    # 3. Create the boolean flag: Is the planet's orbit within the boundaries?
    df['is_habitable_zone'] = (df['pl_orbsmax'] >= df['hz_inner']) & (df['pl_orbsmax'] <= df['hz_outer'])
        
    return df

st.title("?? NASA Exoplanet Habitability Explorer")
st.markdown("Filter and visualize thousands of confirmed exoplanets to identify potential Earth-like candidates.")

df = load_data()

# --- SIDEBAR FILTERS ---
st.sidebar.header("Filter Parameters")

# Distance Filter (applies to everything)
# Fill NaN values with a massive number so they aren't accidentally dropped before filtering
df['sy_dist'] = df['sy_dist'].fillna(999999) 
max_dist = float(df['sy_dist'].max())

max_distance = st.sidebar.slider(
    "Max Distance from Earth (Parsecs)", 
    1.0, 3000.0, 50.0  # Default to a highly local 50 parsecs
)

# The Earth-Like Toggle
earth_like = st.sidebar.toggle("?? Isolate Earth-Like Candidates", value=False)

if earth_like:
    st.sidebar.success("Locked to rocky mass, Earth-size radius, stable star temp, and mature age (>1 Gyr).")
    
    filtered_df = df[
        (df['pl_masse'].between(0.5, 5.0)) &
        (df['pl_rade'].between(0.8, 1.6)) &
        (df['st_teff'].between(2500, 6000)) &
        (df['sy_dist'] <= max_distance) &
        # Filter for mature stars (>1 Gyr) OR keep planets where age is unknown to avoid destroying the dataset
        ((df['st_age'] >= 1.0) | (df['st_age'].isna())) 
    ]
else:
    # Filter by Mass and Temp
    max_mass = float(df['pl_masse'].max())
    mass_range = st.sidebar.slider("Planetary Mass (Earth Masses)", 0.0, 50.0, (0.0, 20.0))
    temp_range = st.sidebar.slider("Host Star Temperature (K)", 2000, 10000, (2000, 7000))

    filtered_df = df[
        (df['pl_masse'] >= mass_range[0]) & (df['pl_masse'] <= mass_range[1]) &
        (df['st_teff'] >= temp_range[0]) & (df['st_teff'] <= temp_range[1]) &
        (df['sy_dist'] <= max_distance)
    ]

# The Habitable Zone Toggle
hz_only = st.sidebar.toggle("?? In Habitable Zone", value=False)

if hz_only:
    # Stack this filter on top of whatever filtered_df currently is
    filtered_df = filtered_df[filtered_df['is_habitable_zone'] == True]

# --- METRICS ---
col1, col2 = st.columns(2)
col1.metric(label="Total Confirmed Planets", value=f"{len(df):,}")
col2.metric(label="Planets Matching Criteria", value=f"{len(filtered_df):,}")

# --- 3D VISUALIZATION & DETAILS PANEL ---
st.subheader("3D Exoplanet Distribution")

if not filtered_df.empty:
    # Split the screen layout (Plot takes 75% width, Details take 25%)
    col_plot, col_details = st.columns([3, 1])
    
    with col_plot:
        fig = px.scatter_3d(
            filtered_df, 
            x='pl_orbper', 
            y='pl_masse', 
            z='pl_rade',
            color='st_teff',
            color_continuous_scale='plasma',
            hover_name='pl_name',
            hover_data={
                'discoverymethod': True, 
                'sy_dist': True, 
                'Star Class': True,     
                'st_teff': False
            },
            labels={
                'pl_orbper': 'Orbital Period (Days)',
                'pl_masse': 'Mass (Earths)',
                'pl_rade': 'Radius (Earths)',
                'sy_dist': 'Distance (Parsecs)'
            }
        )
        
        fig.update_layout(scene=dict(
            xaxis_type="log", 
            yaxis_type="log"
        ), margin=dict(l=0, r=0, b=0, t=0), height=600)
        
        # Capture the click event using on_select="rerun"
        event = st.plotly_chart(
            fig, 
            on_select="rerun", 
            selection_mode="points", 
            use_container_width=True,
            key="planet_plot" 
        )
        
    with col_details:
        st.subheader("Planet Profile")
        
        # 1. Create a list of the currently filtered planet names
        available_planets = filtered_df['pl_name'].tolist()
        
        # 2. Build a searchable dropdown menu
        selected_planet_name = st.selectbox(
            "?? Search or select a planet:", 
            options=available_planets,
            index=0 if available_planets else None
        )
        
        # 3. Display the profile for the selected planet
        if selected_planet_name:
            # Extract that exact row from the dataframe
            planet = filtered_df[filtered_df['pl_name'] == selected_planet_name].iloc[0]
            
            st.markdown(f"### {planet['pl_name']}")
            st.markdown(f"**?? Mass:** {planet['pl_masse']} Earths")
            st.markdown(f"**?? Radius:** {planet['pl_rade']} Earths")
            st.markdown(f"**?? Orbit:** {planet['pl_orbper']} Days")
            st.markdown(f"**?? Distance:** {planet['sy_dist']} Parsecs")
            # --- NEW: Display the ESI ---
            esi_score = float(planet['ESI'])
            st.markdown("---")
            st.markdown(f"**?? Earth Similarity (ESI):** `{esi_score:.2f} / 1.00`")
            
            # Change color based on how high the score is
            if esi_score > 0.8:
                st.info("High probability of Earth-like physical characteristics.")

            st.divider()
            # HZ Display
            hz_status = "? Yes" if planet['is_habitable_zone'] else "? No"
            st.markdown(f"**?? Habitable Zone:** {hz_status}")
            
            if pd.notna(planet['hz_inner']) and pd.notna(planet['hz_outer']) and pd.notna(planet['pl_orbsmax']):
                st.caption(f"Orbit: {planet['pl_orbsmax']:.3f} AU | Zone: {planet['hz_inner']:.3f} - {planet['hz_outer']:.3f} AU")
            
            # Render the progress bar
            st.progress(esi_score)
            st.divider()
            st.markdown(f"**?? Discovery:** {planet['discoverymethod']} ({planet['disc_year']})")
            st.markdown(f"**?? Star:** {planet['Star Class']}")
            # Format the age, handling NaN values cleanly
            age_display = f"{planet['st_age']} Billion Years" if pd.notna(planet['st_age']) else "Unknown"
            st.markdown(f"**? Star Age:** {age_display}")
            
            st.divider()
            # Generate the URL-safe name and create a button
            safe_planet_name = urllib.parse.quote(planet['pl_name'])
            nasa_url = f"https://exoplanetarchive.ipac.caltech.edu/overview/{safe_planet_name}"
            
            st.link_button("?? View on NASA Exoplanet Archive", nasa_url, use_container_width=True)
        else:
            # The default message before the user clicks anything
            st.info("?? Click on any planet in the 3D plot to lock its profile here.")
            
else:
    st.warning("No planets match your current filter criteria.")

# --- DATA TABLE ---
st.subheader("Filtered Dataset")
st.dataframe(filtered_df)