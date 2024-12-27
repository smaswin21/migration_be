from flask import Flask
from flask_cors import CORS
from api.routes import api_blueprint

# Initialize Flask app
app = Flask(__name__)

# Enable Cross-Origin Resource Sharing
CORS(app)

# Register blueprints for modularity
app.register_blueprint(api_blueprint, url_prefix='/api')

if __name__ == '__main__':
    app.run(debug=True)
