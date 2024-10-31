from flask import Blueprint, request, jsonify
from services.auth_service import register_user, login_user, start_google_login, handle_google_callback
from flask_jwt_extended import jwt_required

auth_bp = Blueprint('auth', __name__)

@auth_bp.route('/register', methods=['POST'])
def register():
    data = request.get_json()
    register_user(data['username'], data['password'])
    return jsonify({'msg': 'User registered successfully'}), 201

@auth_bp.route('/login', methods=['POST'])
def login():
    data = request.get_json()
    token = login_user(data['username'], data['password'])
    if token:
        return jsonify({'access_token': token}), 200
    return jsonify({'msg': 'Login failed. Check credentials and try again.'}), 401

@auth_bp.route('/login/google')
def login_with_google():
    return start_google_login()

@auth_bp.route('/auth/callback')
def oauth_callback():
    token = handle_google_callback()
    if token:
        return jsonify({'access_token': token}), 200
    return jsonify({'msg': 'Login failed. Check credentials and try again.'}), 401
