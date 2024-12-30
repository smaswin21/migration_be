import pandas as pd
import folium
from folium.plugins import MarkerCluster, HeatMap
import os

def preprocess_data(file_path):
    """Load and preprocess the migration dataset."""
    df = pd.read_csv(file_path)

    # Filter data for 2024
    df = df[df['Incident Year'] == 2024]

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

    # Add a MarkerCluster
    marker_cluster = MarkerCluster().add_to(base_map)
    for _, row in df.iterrows():
        tooltip = f"""
        <strong>Incident:</strong> {row['Incident Type']}<br>
        <strong>Migration Route:</strong> {row['Migration Route']}<br>
        <strong>Region:</strong> {row['Region of Incident']}<br>
        <strong>Total Dead and Missing:</strong> {row['Total Number of Dead and Missing']}
        """
        folium.Marker(
            location=[row['Latitude'], row['Longitude']],
            tooltip=tooltip
        ).add_to(marker_cluster)

    # Add a heatmap
    heat_data = df[['Latitude', 'Longitude', 'Total Number of Dead and Missing']].dropna().values.tolist()
    HeatMap(heat_data, radius=15, blur=10, max_zoom=1).add_to(base_map)

    os.makedirs('results', exist_ok=True)
    map_path = 'results/map_2024.html'
    base_map.save(map_path)

    return map_path
