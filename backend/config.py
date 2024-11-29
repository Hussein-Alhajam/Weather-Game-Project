from datetime import timedelta
import os

class Config:
    # Weather and IP information
    WEATHER_API_KEY = os.environ.get('WEATHER_API_KEY') or '37052376f3e84317b1f54312243110'
    
    # Secret Keys
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'supersecretkey'
    JWT_SECRET_KEY = os.environ.get('JWT_SECRET_KEY') or 'superjwtsecretkey'
    
    # Setting to control token expiry
    JWT_ACCESS_TOKEN_EXPIRES = timedelta(hours=3)    # Access token expires in 3 hour
    JWT_REFRESH_TOKEN_EXPIRES = timedelta(days=1)    # Refresh token expires in 1 day

    # SQLAlchemy Database Configuration
    SQLALCHEMY_DATABASE_URI = 'sqlite:///game.db'
    SQLALCHEMY_TRACK_MODIFICATIONS = False

    # Google OAuth Configuration
    GOOGLE_CLIENT_ID = os.environ.get('GOOGLE_CLIENT_ID') or '511564159141-sr24p4cdqo7jlrfohv2crlrgepc10ent.apps.googleusercontent.com'
    GOOGLE_CLIENT_SECRET = os.environ.get('GOOGLE_CLIENT_SECRET') or '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'
    GOOGLE_DISCOVERY_URL = "https://accounts.google.com/.well-known/openid-configuration"

    # Ensure essential environment variables are set in production
    if not GOOGLE_CLIENT_ID or not GOOGLE_CLIENT_SECRET:
        raise ValueError("Google OAuth credentials are not set in the environment.")
