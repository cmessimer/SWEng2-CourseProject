from inventory_management import app, db  # Import Flask app and database

with app.app_context():
    db.create_all()
    print("Database initialized successfully!")
