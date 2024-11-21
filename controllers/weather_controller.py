from flask import Blueprint, jsonify, request
from services.weather_service import get_real_weather
import logging

weather_bp = Blueprint('weather', __name__)
logging.basicConfig(level=logging.INFO)

@weather_bp.route('/get_weather', methods=['GET'])
def get_weather():
    """API endpoint to fetch weather data for the user’s current location."""
    location = request.args.get('location', 'Oshawa, Canada')

    if not location or not isinstance(location, str):
        logging.error(f"Invalid location parameter: {location}")
        return jsonify({'msg': 'Invalid location parameter'}), 400

    try:
        weather_data = get_real_weather(location)
        if weather_data:
            return jsonify(weather_data), 200
        return jsonify({'msg': 'Failed to retrieve weather data'}), 400
    except Exception as e:
        logging.error(f"Error fetching weather data: {e}")
        return jsonify({'msg': 'Error fetching weather data'}), 500
