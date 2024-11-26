from werkzeug.security import generate_password_hash, check_password_hash
from flask_jwt_extended import create_access_token
from flask import redirect, session, url_for
from extensions import db, google
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
def handle_google_callback():
    try:
        # Attempt to get the token and parse the user information
        token = google.authorize_access_token()
        user_info = google.parse_id_token(token, nonce=session.get('nonce'))
        user = User.query.filter_by(email=user_info['email']).first()

        # Attempt to find the user by email in the database
        if not user:
            # Create a new user if one does not exist
            user = User(username=user_info['name'], email=user_info['email'])
            db.session.add(user)
            db.session.commit()

        # Generate and return an access token for the user
        logging.info(f"User {user_info['name']} logged in via Google.")
        return create_access_token(identity=str(user.username), additional_claims={"user_id": str(user.id)})

    except Exception as e:
        # Log any errors that occur during the process
        logging.error(f"Google OAuth error: {e}")
        return None
