from flask import Flask, render_template
from flask_sqlalchemy import SQLAlchemy
from flask_jwt_extended import JWTManager
from flask_migrate import Migrate
from config import Config
from models import db
from routes import api_routes

# Initialize Flask App
app = Flask(__name__)
app.config.from_object(Config)  # Load database & JWT configuration

# Initialize Flask Extensions
app = Flask(__name__)
app.config.from_object(Config)

# Initialize Flask Extensions
db.init_app(app)
jwt = JWTManager(app)
migrate = Migrate(app, db)  # Ensures database migration works

# Register API Routes
app.register_blueprint(api_routes)  # 📌 Ensure Blueprint is registered!

if __name__ == '__main__':
    with app.app_context():
        db.create_all()
    app.run(debug=True)
