from werkzeug.security import generate_password_hash, check_password_hash
from flask_jwt_extended import create_access_token
from extensions import db
from models.user_model import User
import logging

# Initialize logging
logging.basicConfig(level=logging.INFO)

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

# Login User
def login_user(username, password):
    try:
        user = User.query.filter_by(username=username).first()
        if user and check_password_hash(user.password, password):
            # Convert user ID to a string explicitly
            token = create_access_token(identity=user.username, additional_claims={"user_id": user.id})
            logging.info(f"User {username} logged in successfully.")
            return token
        else:
            logging.warning(f"Login failed for user {username}: Invalid credentials.")
            return None
    except Exception as e:
        logging.error(f"Error during login for user {username}: {e}")
        return None

# Handle Google OAuth Callback
def handle_google_callback(google):
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
