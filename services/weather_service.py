import requests
from config import Config
from flask import request
import logging

logging.basicConfig(level=logging.INFO)

def get_user_ip():
    return request.headers.get('X-Forwarded-For', request.remote_addr)

def get_location_from_ip(ip_address):
    url = f'http://ipinfo.io/{ip_address}/json?token={Config.IPINFO_TOKEN}'
    try:
        response = requests.get(url)
        response.raise_for_status()
        location_data = response.json()
        return location_data.get('city')
    except requests.RequestException as e:
        logging.error(f"Error retrieving location for IP {ip_address}: {e}")
        return None

def get_real_weather(location):
    url = f'http://api.weatherapi.com/v1/current.json?key={Config.WEATHER_API_KEY}&q={location}'
    try:
        response = requests.get(url)
        response.raise_for_status()
        return response.json()
    except requests.RequestException as e:
        logging.error(f"Error retrieving weather for location {location}: {e}")
        return None
