from flask import Blueprint, request, jsonify, session, url_for
from services.auth_service import register_user, login_user, handle_google_callback
from flask_jwt_extended import jwt_required, get_jwt_identity
from extensions import google
import logging
import os

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
    nonce = os.urandom(16).hex()  # Randomly generate a nonce
    session['nonce'] = nonce
    redirect_uri = url_for('auth.oauth_callback', _external=True)
    return google.authorize_redirect(redirect_uri, nonce=nonce)

@auth_bp.route('/callback', methods=['GET'])
def oauth_callback():
    try:
        token = handle_google_callback()
        if token:
            return jsonify({'access_token': token}), 200
        logging.warning("Google OAuth failed: No token received")
        return jsonify({'msg': 'Google OAuth failed'}), 401
    except Exception as e:
        logging.error(f"Error during Google OAuth callback: {e}")
        return jsonify({'msg': 'Google OAuth error'}), 500
