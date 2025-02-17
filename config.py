import os

class Config:
    # database location using SQLite
    SQLALCHEMY_DATABASE_URI = "sqlite:///./app.db"  # Saves in project root
    SQLALCHEMY_TRACK_MODIFICATIONS = False  # Disables unnecessary warning logs

    # Load JWT secret key securely from environment variables
    JWT_SECRET_KEY = os.getenv("JWT_SECRET", "fallback_secret_if_not_set")

    # Email configuration (For notifications)
    SMTP_SERVER = os.getenv("SMTP_SERVER", "smtp.example.com")
    SMTP_PORT = int(os.getenv("SMTP_PORT", 587))
    SMTP_EMAIL = os.getenv("SMTP_EMAIL", "your_email@example.com")
    SMTP_PASSWORD = os.getenv("SMTP_PASSWORD", "your_email_password")
