from flask import Flask, render_template
from flask_sqlalchemy import SQLAlchemy
from flask_jwt_extended import JWTManager
from flask_migrate import Migrate
from config import Config
from models import db  # Import models but don't initialize db yet

# Initialize Flask App
app = Flask(__name__)
app.config.from_object(Config)  # Load database & JWT configuration

# Initialize Flask Extensions
db.init_app(app)  # Only initialize here
jwt = JWTManager(app)
migrate = Migrate(app, db)  # Ensures database migration works

# Import routes AFTER app & db are initialized to avoid circular import
from routes import api_routes
app.register_blueprint(api_routes)  # Ensure Blueprint is registered!

# Serve the frontend (optional, if using templates)
@app.route('/')
def home():
    return render_template("index.html")

if __name__ == '__main__':
    with app.app_context():
        db.create_all()
    app.run(debug=True)
