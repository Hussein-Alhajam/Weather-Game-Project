from flask import Blueprint, request, jsonify
from services.auth_service import register_user, login_user, handle_google_callback
from flask_jwt_extended import jwt_required
from extensions import google
import logging

auth_bp = Blueprint('auth', __name__)
logging.basicConfig(level=logging.INFO)

@auth_bp.route('/register', methods=['POST'])
def register():
    data = request.get_json()
    if not data or 'username' not in data or 'password' not in data:
        logging.error("Registration failed: Missing username or password")
        return jsonify({'msg': 'Username and password are required'}), 400

    try:
        register_user(data['username'], data['password'])
        return jsonify({'msg': 'User registered successfully'}), 201
    except Exception as e:
        logging.error(f"Error registering user: {e}")
        return jsonify({'msg': 'Error registering user'}), 500

@auth_bp.route('/login', methods=['POST'])
def login():
    data = request.get_json()
    if not data or 'username' not in data or 'password' not in data:
        logging.error("Login failed: Missing username or password")
        return jsonify({'msg': 'Username and password are required'}), 400

    try:
        token = login_user(data['username'], data['password'])
        if token:
            return jsonify({'access_token': token}), 200
        logging.warning(f"Login failed: Invalid credentials for user {data['username']}")
        return jsonify({'msg': 'Invalid credentials'}), 401
    except Exception as e:
        logging.error(f"Error during login: {e}")
        return jsonify({'msg': 'Error during login'}), 500

@auth_bp.route('/login/google', methods=['GET'])
def login_with_google():
    try:
        return google.authorize_redirect(redirect_uri='/auth/callback')
    except Exception as e:
        logging.error(f"Error starting Google login: {e}")
        return jsonify({'msg': 'Error starting Google login'}), 500

@auth_bp.route('/auth/callback')
def oauth_callback():
    try:
        # Pass `google` to handle the Google callback
        token = handle_google_callback(google)
        if token:
            return jsonify({'access_token': token}), 200
        logging.warning("Google OAuth failed: No token received")
        return jsonify({'msg': 'Google OAuth failed'}), 401
    except Exception as e:
        logging.error(f"Error during Google OAuth callback: {e}")
        return jsonify({'msg': 'Google OAuth error'}), 500
