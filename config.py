import os

class Config:
    WEATHER_API_KEY = os.environ.get('WEATHER_API_KEY') or '37052376f3e84317b1f54312243110'
    IPINFO_TOKEN = os.environ.get('IPINFO_TOKEN') or 'your_ipinfo_token'
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'supersecretkey'
    SQLALCHEMY_DATABASE_URI = 'sqlite:///game.db'
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    JWT_SECRET_KEY = os.environ.get('JWT_SECRET_KEY') or 'superjwtsecretkey'
