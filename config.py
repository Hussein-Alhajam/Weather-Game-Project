import os

class Config:
    # Weather and IP information
    WEATHER_API_KEY = os.environ.get('WEATHER_API_KEY') or '37052376f3e84317b1f54312243110'
    
    # Secret Keys
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'supersecretkey'
    JWT_SECRET_KEY = os.environ.get('JWT_SECRET_KEY') or 'superjwtsecretkey'

    # SQLAlchemy Database Configuration
    SQLALCHEMY_DATABASE_URI = 'sqlite:///game.db'  # For local development, use SQLite
    SQLALCHEMY_TRACK_MODIFICATIONS = False

    # Google OAuth Configuration
    GOOGLE_CLIENT_ID = os.environ.get('GOOGLE_CLIENT_ID') or 'your_google_client_id'
    GOOGLE_CLIENT_SECRET = os.environ.get('GOOGLE_CLIENT_SECRET') or 'your_google_client_secret'
    GOOGLE_DISCOVERY_URL = "https://accounts.google.com/.well-known/openid-configuration"

    # Ensure essential environment variables are set in production
    if not GOOGLE_CLIENT_ID or not GOOGLE_CLIENT_SECRET:
        raise ValueError("Google OAuth credentials are not set in the environment.")
