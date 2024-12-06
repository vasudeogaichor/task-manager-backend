from flask_pymongo import PyMongo

mongo = PyMongo()

def configure_app(app):
    app.config['SECRET_KEY'] = '<secret_key>'
    app.config['MONGO_URI'] = '<mongo_uri>'
    # app.config['MONGO_URI'] = 'mongodb://vasudeogaichor:vasudeogaichor@localhost:27017/task-management'
    
    mongo.init_app(app)
    with app.app_context():
        try:
            # Trigger a simple operation to confirm connection
            mongo.db.list_collection_names()
            print("Successfully connected to MongoDB.")
        except Exception as e:
            print(f"Failed to connect to MongoDB: {e}")
            raise
