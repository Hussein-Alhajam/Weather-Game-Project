from werkzeug.security import generate_password_hash, check_password_hash
from flask_jwt_extended import create_access_token
from authlib.integrations.flask_client import OAuth
from models.user_model import User
from app import db, app
import logging

# Initialize logging
logging.basicConfig(level=logging.INFO)

# Initialize OAuth
oauth = OAuth(app)
google = oauth.register(
    name='google',
    client_id=app.config['GOOGLE_CLIENT_ID'],
    client_secret=app.config['GOOGLE_CLIENT_SECRET'],
    access_token_url='https://accounts.google.com/o/oauth2/token',
    authorize_url='https://accounts.google.com/o/oauth2/auth',
    client_kwargs={'scope': 'openid email profile'},
)

def register_user(username, password):
    try:
        hashed_password = generate_password_hash(password)
        new_user = User(username=username, password=hashed_password)
        db.session.add(new_user)
        db.session.commit()
        logging.info(f"User {username} registered successfully.")
    except Exception as e:
        db.session.rollback()
        logging.error(f"Error registering user {username}: {e}")

def handle_google_callback():
    try:
        token = google.authorize_access_token()
        user_info = google.parse_id_token(token)
        user = User.query.filter_by(email=user_info['email']).first()
        if not user:
            user = User(username=user_info['name'], email=user_info['email'])
            db.session.add(user)
            db.session.commit()
        logging.info(f"User {user_info['name']} logged in via Google.")
        return create_access_token(identity=user.id)
    except Exception as e:
        logging.error(f"Google OAuth error: {e}")
        return None
