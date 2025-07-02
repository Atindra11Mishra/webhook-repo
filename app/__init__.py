import os
from flask import Flask
from dotenv import load_dotenv
from .extensions import mongo
from .webhook.routes import webhook

def create_app():
    # Load environment variables from .env file
    load_dotenv()
    
    app = Flask(__name__)

    # Configuration from environment variables
    app.config["MONGO_URI"] = os.getenv("MONGO_URI")
    
    # Validate required environment variables
    if not app.config["MONGO_URI"]:
        raise ValueError("MONGO_URI environment variable is required")

    # Initialize extensions
    mongo.init_app(app)

    # Register blueprints
    app.register_blueprint(webhook)

    return app