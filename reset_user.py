from app import db, app
from models import User
from werkzeug.security import generate_password_hash

with app.app_context():
    user = User.query.filter_by(username="chad").first()
    if user:
        db.session.delete(user)
        db.session.commit()
        print("User 'chad' deleted.")

    # ✅ Now recreate user with hashed password
    new_user = User(
        username="chad",
        password=generate_password_hash("newpassword456"),
        position="Employee",
        role="Employee"
    )
    db.session.add(new_user)
    db.session.commit()
    print("✅ User 'chad' created successfully!")
    print("Database reset complete.")
    print("User 'chad' is now ready for use.")
    print("Please log in with the new credentials.")
    print("Username: chad")
    
