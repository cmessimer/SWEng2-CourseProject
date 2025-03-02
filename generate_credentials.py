import secrets
import string
from werkzeug.security import generate_password_hash
from app import db, app
from models import User

# Generate Secure Random Password
def generate_secure_password(length=12):
    characters = string.ascii_letters + string.digits + string.punctuation
    return ''.join(secrets.choice(characters) for _ in range(length))

with app.app_context():
    user = User.query.filter_by(username="chad").first()
    if user:
        new_password = generate_secure_password()  # Generate a new password
        hashed_password = generate_password_hash(new_password)  # Hash the password

        user.password = hashed_password  # Store hashed password
        db.session.commit()

        print(f"Password reset successfully!\n New Password: {new_password}")
    else:
        print("User 'chad' not found.")
