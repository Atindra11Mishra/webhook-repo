import os
from dotenv import load_dotenv
from app import create_app

# Load environment variables
load_dotenv()

# Create Flask app
app = create_app()

if __name__ == "__main__":
    # Get port from environment or use default
    port = int(os.getenv("FLASK_PORT", 5000))
    debug = os.getenv("FLASK_DEBUG", "False").lower() == "true"
    
    app.run(
        host="0.0.0.0",
        port=port,
        debug=debug
    )