from flask import Blueprint, redirect, request, jsonify, session, url_for
from services import auth_service
from services.auth_service import register_user, login_user, handle_google_callback
from flask_jwt_extended import jwt_required, get_jwt_identity
from extensions import google
import logging
import os

auth_bp = Blueprint('auth', __name__)
logging.basicConfig(level=logging.INFO)

@auth_bp.route('/register', methods=['POST'])
def register():
    data = request.form
    username = data.get('username')
    email = data.get('email')
    password = data.get('password')

    if not username or not email or not password:
        return jsonify({'msg': 'All fields are required'}), 400

    # Use the auth_service to handle registration
    try:
        new_user = register_user(username, email, password)
        return jsonify({'msg': 'Registration successful', 'user_id': new_user.id}), 201
    except ValueError as e:
        return jsonify({'msg': str(e)}), 400
    except Exception as e:
        logging.error(f"Error during registration: {e}")
        return jsonify({'msg': 'Registration failed'}), 500


@auth_bp.route('/login', methods=['POST'])
def login():
    data = request.form
    username = data.get('username')
    password = data.get('password')

    if not username or not password:
        return jsonify({'msg': 'Username and password are required'}), 400

    token = login_user(username, password)
    if token:
        return jsonify({'access_token': token}), 200
    return jsonify({'msg': 'Invalid credentials'}), 401

@auth_bp.route('/login/google', methods=['GET'])
def login_with_google():
    nonce = os.urandom(16).hex()  # Randomly generate a nonce
    session['nonce'] = nonce
    redirect_uri = url_for('auth.oauth_callback', _external=True)
    return google.authorize_redirect(redirect_uri, nonce=nonce)

@auth_bp.route('/callback', methods=['GET'])
def oauth_callback():
    try:
        token = auth_service.handle_google_callback()
                
        # Redirect to frontend with token in query params
        return redirect(f"/auth/success?access_token={token}")
    except Exception as e:
        logging.error(f"Error during Google OAuth callback: {e}")
        return redirect("/auth/error")

