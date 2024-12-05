from flask import Flask
from app.config import configure_app
from app.routes import register_routes

# Initialize the Flask app
app = Flask(__name__)

# Configure the app
configure_app(app)

# Register routes
register_routes(app)

if __name__ == "__main__":
    app.run(debug=True)
