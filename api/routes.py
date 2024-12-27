from flask import Blueprint, jsonify
from api.utils import preprocess_data, generate_visualizations

api_blueprint = Blueprint('api', __name__)

# Load and preprocess the dataset
data_path = '/Users/sm_aswin21/Desktop/migration_be/data/Missing Migrants Global Figures.csv'
preprocessed_data = preprocess_data(data_path)

@api_blueprint.route('/migration-data', methods=['GET'])
def get_migration_data():
    """Serve migration data to the frontend."""
    data = preprocessed_data[['Latitude', 'Longitude', 'Total Number of Dead and Missing',
                              'Incident Type', 'Region of Incident', 'Incident Date']].to_dict(orient='records')
    return jsonify(data)

@api_blueprint.route('/generate-map', methods=['GET'])
def generate_map():
    """Generate a Folium map and save as an HTML file."""
    map_path = generate_visualizations(preprocessed_data)
    return jsonify({'map_path': map_path})
