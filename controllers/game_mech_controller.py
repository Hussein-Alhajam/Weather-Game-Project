from flask import Blueprint, jsonify, request
from flask_jwt_extended import jwt_required, get_jwt_identity
from services.game_service import (
    apply_weather_effects,
    initialize_game_room,
    load_game,
    save_game,
    update_game_state,
    update_gameplay_weather,
    update_player_stats,
    reset_player_stats,
    get_room_state,
    get_player_state,
)
import logging

from services.weather_service import get_location_from_ip, get_weather_for_location

logging.basicConfig(level=logging.INFO)

game_mech_bp = Blueprint('game_mechanics', __name__)

# --- Room State Endpoints ---


@game_mech_bp.route('/room/initialize', methods=['POST'])
@jwt_required()
def initialize_room():
    """API to initialize a game room with resources and inventory."""
    data = request.get_json()

    room_id = data.get("room_id")
    players = data.get("players", [])  # List of player IDs
    initial_resources = data.get("resources", [])  # List of resources
    initial_inventory = data.get("inventory", {})  # Dictionary of user_id -> inventory items

    if not room_id or not players:
        return jsonify({"msg": "Room ID and players are required."}), 400

    try:
        result = initialize_game_room(room_id, players, initial_resources, initial_inventory)
        return jsonify(result), 200
    except Exception as e:
        return jsonify({"msg": f"Error initializing room: {e}"}), 500


@game_mech_bp.route('/room/state/<int:room_id>', methods=['GET'])
@jwt_required()
def get_room_state_endpoint(room_id):
    """Get the current state of the room (Day/Night)."""
    try:
        room_state = get_room_state(room_id)
        if not room_state:
            return jsonify({'msg': f'Room with ID {room_id} not found'}), 404
        return jsonify(room_state), 200
    except Exception as e:
        logging.error(f"Error fetching room state for room {room_id}: {e}")
        return jsonify({'msg': 'Error fetching room state'}), 500

@game_mech_bp.route('/room/state/<int:room_id>', methods=['PUT'])
@jwt_required()
def update_room_state_endpoint(room_id):
    """Manually trigger an update of the room's state."""
    try:
        current_state = update_game_state(room_id)
        if not current_state:
            return jsonify({'msg': f'Room with ID {room_id} not found'}), 404
        return jsonify({'msg': f'Room state updated to {current_state}'}), 200
    except Exception as e:
        logging.error(f"Error updating room state for room {room_id}: {e}")
        return jsonify({'msg': 'Error updating room state'}), 500

# --- Player State Endpoints ---

@game_mech_bp.route('/player/state/<int:user_id>', methods=['GET'])
@jwt_required()
def get_player_state_endpoint(user_id):
    """Get the current state of the player (Hunger, Health and Sanity)."""
    try:
        player_state = get_player_state(user_id)
        if not player_state:
            return jsonify({'msg': f'Player with ID {user_id} not found'}), 404
        return jsonify(player_state), 200
    except Exception as e:
        logging.error(f"Error fetching player state for player {user_id}: {e}")
        return jsonify({'msg': 'Error fetching player state'}), 500

@game_mech_bp.route('/player/state/<int:user_id>', methods=['PUT'])
@jwt_required()
def update_player_state_endpoint(user_id):
    """Manually trigger an update of the player's state."""
    try:
        updated_state = update_player_stats(user_id)
        if not updated_state:
            return jsonify({'msg': f'Player with ID {user_id} not found'}), 404
        return jsonify({'msg': 'Player state updated successfully'}), 200
    except Exception as e:
        logging.error(f"Error updating player state for player {user_id}: {e}")
        return jsonify({'msg': 'Error updating player state'}), 500

@game_mech_bp.route('/player/state/<int:user_id>/reset', methods=['POST'])
@jwt_required()
def reset_player_state_endpoint(user_id):
    """Reset the player's stats (Hunger, Health and Sanity)."""
    try:
        reset_state = reset_player_stats(user_id)
        if not reset_state:
            return jsonify({'msg': f'Player with ID {user_id} not found'}), 404
        return jsonify({'msg': 'Player state reset successfully'}), 200
    except Exception as e:
        logging.error(f"Error resetting player state for player {user_id}: {e}")
        return jsonify({'msg': 'Error resetting player state'}), 500

# --- Weather Effects Endpoint ---
@game_mech_bp.route('/weather/effects', methods=['POST'])
@jwt_required()
def apply_weather_effects_endpoint():
    """
    Apply weather effects to players based on real-time weather data.
    """
    try:
        # Get the current user's IP address
        ip_address = request.headers.get('X-Forwarded-For', request.remote_addr)

        # If running locally, replace 127.0.0.1 for testing purposes
        if ip_address == '127.0.0.1':
            ip_address = '192.197.54.32'  # UOIT IP for testing

        # Fetch location using the weather_service
        lat, lon = get_location_from_ip(ip_address)
        if not lat or not lon:
            logging.error(f"Failed to determine location for IP {ip_address}")
            return jsonify({'msg': 'Could not determine location from IP'}), 400

        # Fetch weather data for the location
        weather_data = get_weather_for_location(lat, lon)
        if not weather_data:
            return jsonify({'msg': 'Failed to retrieve weather data'}), 500

        # Apply weather effects using the game_service logic
        apply_weather_effects_to_all_players(weather_data)

        return jsonify({
            'msg': 'Weather effects applied successfully',
            'weather_data': weather_data
        }), 200
    except Exception as e:
        logging.error(f"Error applying weather effects: {e}")
        return jsonify({'msg': 'Error applying weather effects'}), 500


def apply_weather_effects_to_all_players(weather_data):
    """
    Apply weather effects to all players in the game based on weather conditions.
    """
    from models.player_state import PlayerState

    # Query all players' states
    players = PlayerState.query.all()
    for player in players:
        apply_weather_effects(player, weather_data)
        logging.info(f"Applied weather effects for player {player.user_id}")


# --- Save and Load Endpoint ---

@game_mech_bp.route('/save', methods=['POST'])
@jwt_required()
def save_game_state():
    """Save the current game state for the authenticated user."""
    try:
        user_id = get_jwt_identity()
        success = save_game(user_id)
        if success:
            return jsonify({'msg': 'Game state saved successfully'}), 200
        return jsonify({'msg': 'Failed to save game state'}), 500
    except Exception as e:
        logging.error(f"Error saving game state: {e}")
        return jsonify({'msg': 'Error saving game state'}), 500


@game_mech_bp.route('/load', methods=['GET'])
@jwt_required()
def load_game_state():
    """Load the saved game state for the authenticated user."""
    try:
        # Get the authenticated user's ID
        user_id = get_jwt_identity()
        
        # Get `save_id` from query parameters
        save_id = request.args.get('save_id')
        if not save_id:
            return jsonify({'msg': 'Missing save_id parameter'}), 400

        # Call the `load_game` function with `user_id` and `save_id`
        game_state = load_game(user_id, save_id)
        if game_state:
            return jsonify({'msg': 'Game state loaded successfully', 'game_state': game_state.to_dict()}), 200
        return jsonify({'msg': 'No saved game state found'}), 404
    except Exception as e:
        logging.error(f"Error loading game state: {e}")
        return jsonify({'msg': 'Error loading game state'}), 500
