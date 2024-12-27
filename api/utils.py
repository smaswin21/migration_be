import pandas as pd
import folium
from folium.plugins import HeatMap
import os

def preprocess_data(file_path):
    """Load and preprocess the migration dataset."""
    df = pd.read_csv(file_path)

    # Handle missing values
    df = df.dropna(subset=['Coordinates'])
    df['Incident Date'] = df['Incident Date'].fillna('Unknown_Date')
    df['Cause of Death'] = df['Cause of Death'].fillna('Unknown')
    df['Migration Route'] = df['Migration Route'].fillna('Unknown')
    df['Country of Origin'] = df['Country of Origin'].fillna('Unknown')
    df['Region of Origin'] = df['Region of Origin'].fillna('Unknown')
    df['Information Source'] = df['Information Source'].fillna('Unknown')

    numerical_cols = [
        'Number of Dead', 'Minimum Estimated Number of Missing', 
        'Number of Survivors', 'Number of Females', 
        'Number of Males', 'Number of Children'
    ]
    df[numerical_cols] = df[numerical_cols].fillna(0).astype(int)

    # Extract latitude and longitude
    df[['Latitude', 'Longitude']] = df['Coordinates'].str.split(', ', expand=True).astype(float)

    return df


def generate_visualizations(df):
    """Generate a Folium map and save it as an HTML file."""
    base_map = folium.Map(location=[20, 10], zoom_start=2)

    for _, row in df.iterrows():
        tooltip = f"Incident: {row['Incident Type']}<br>Region: {row['Region of Incident']}<br>Fatalities: {row['Total Number of Dead and Missing']}"
        folium.CircleMarker(
            location=[row['Latitude'], row['Longitude']],
            radius=5,
            color='red',
            fill=True,
            fill_opacity=0.6,
            tooltip=tooltip
        ).add_to(base_map)

    heat_data = df[['Latitude', 'Longitude', 'Total Number of Dead and Missing']].dropna().values.tolist()
    HeatMap(heat_data, radius=15, blur=10, max_zoom=1).add_to(base_map)

    os.makedirs('results', exist_ok=True)
    map_path = 'results/map_overview_1.html'
    base_map.save(map_path)

    return map_path