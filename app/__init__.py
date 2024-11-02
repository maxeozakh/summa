from flask import Flask
from flask_cors import CORS  # Import the CORS extension

def create_app():
    app = Flask(__name__)

    # Enable CORS for all origins on all routes
    CORS(app, resources={r"/*": {"origins": "*"}})

    # Import routes
    from app.routes import summarize

    # Register routes
    app.register_blueprint(summarize)

    return app
