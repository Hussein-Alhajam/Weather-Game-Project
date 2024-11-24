from flask import Blueprint, jsonify, request
from services.weather_service import get_location_from_ip, get_weather_for_location
import logging
from flask_jwt_extended import jwt_required, get_jwt_identity

weather_bp = Blueprint('weather', __name__)
logging.basicConfig(level=logging.INFO)

@weather_bp.route('/current', methods=['GET'])
@jwt_required()
def current_weather():
    """API endpoint to fetch weather data for the user’s current location."""
    # Get the current user's identity from the JWT token
    user_identity = get_jwt_identity()
    
    ip_address = request.headers.get('X-Forwarded-For', request.remote_addr)

    # If running locally, replace 127.0.0.1 for testing purposes
    if ip_address == '127.0.0.1':
        ip_address = '192.197.54.32' # UOIT IP

    # Log user identity and IP address
    logging.info(f"User {user_identity} with IP address {ip_address} is requesting weather data.")

    # Get user's latitude and longitude based on IP address
    lat, lon = get_location_from_ip(ip_address)
    if not lat or not lon:
        logging.error(f"Failed to determine location for IP {ip_address}")
        return jsonify({'msg': 'Could not determine location from IP'}), 400

    # Get weather data using the latitude and longitude
    try:
        weather_data = get_weather_for_location(lat, lon)
        if weather_data:
            return jsonify({'user': user_identity, 'weather': weather_data}), 200
        return jsonify({'msg': 'Failed to retrieve weather data'}), 400
    except Exception as e:
        logging.error(f"Error fetching weather data: {e}")
        return jsonify({'msg': 'Error fetching weather data'}), 500
