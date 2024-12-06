from flask import Flask
from app.config import configure_app
from app.routes import register_routes

app = Flask(__name__)

configure_app(app)
register_routes(app)

if __name__ == "__main__":
    app.run(debug=True)
