from flask import Blueprint, jsonify
from services.weather_service import get_weather_for_user

weather_bp = Blueprint('weather', __name__)

@weather_bp.route('/get_weather', methods=['GET'])
def get_weather():
    """API endpoint to fetch weather data for the user’s current location."""
    weather_data = get_weather_for_user()
    if weather_data:
        return jsonify(weather_data), 200
    return jsonify({'msg': 'Failed to retrieve weather data'}), 400
