import requests
import logging
from config import Config

logging.basicConfig(level=logging.INFO)

def get_location_from_ip(ip_address):
    """Fetches the user's location from IP address using WeatherAPI."""
    API_KEY = Config.WEATHER_API_KEY  # WeatherAPI key for IP geolocation
    url = f'http://api.weatherapi.com/v1/ip.json?key={API_KEY}&q={ip_address}'
    try:
        response = requests.get(url)
        response.raise_for_status()
        location_data = response.json()
        lat = location_data.get('lat')
        lon = location_data.get('lon')
        if lat and lon:
            return lat, lon
        logging.error(f"Failed to retrieve valid location for IP {ip_address}")
    except requests.RequestException as e:
        logging.error(f"Error retrieving location for IP {ip_address}: {e}")
    return None, None

def get_weather_for_location(lat, lon):
    """Fetches weather data based on latitude and longitude using WeatherAPI."""
    WEATHER_API_KEY = Config.WEATHER_API_KEY
    url = f'http://api.weatherapi.com/v1/current.json?key={WEATHER_API_KEY}&q={lat},{lon}'
    try:
        response = requests.get(url)
        response.raise_for_status()
        return response.json()
    except requests.RequestException as e:
        logging.error(f"Error retrieving weather for location ({lat}, {lon}): {e}")
        return None
