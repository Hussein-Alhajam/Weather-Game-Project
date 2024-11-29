from werkzeug.security import generate_password_hash, check_password_hash
from flask_jwt_extended import create_access_token
from flask import redirect, session, url_for
from backend.extensions import db, google
from models.user_model import User
import logging

# Initialize logging
logging.basicConfig(level=logging.INFO)

def register_user(username, email, password):
    # Check if username or email already exists
    if User.query.filter_by(username=username).first():
        raise ValueError('Username already exists')
    if User.query.filter_by(email=email).first():
        raise ValueError('Email already exists')

    # Create a new user and hash the password
    hashed_password = generate_password_hash(password)
    new_user = User(username=username, email=email, password=hashed_password)

    db.session.add(new_user)
    db.session.commit()

    return new_user


# Login User
def login_user(username, password):
    user = User.query.filter_by(username=username).first()
    if user and check_password_hash(user.password, password):
        return create_access_token(identity=str(user.username), additional_claims={"user_id": str(user.id)})
    return None

# Handle Google OAuth Callback
def handle_google_callback():
    token = google.authorize_access_token()
    user_info = google.parse_id_token(token)
    user = User.query.filter_by(email=user_info['email']).first()
    if not user:
        user = User(username=user_info['name'], email=user_info['email'])
        db.session.add(user)
        db.session.commit()
    return create_access_token(identity=str(user.username), additional_claims={"user_id": str(user.id)})