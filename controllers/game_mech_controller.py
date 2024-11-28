from flask import Blueprint, jsonify, request
from flask_jwt_extended import jwt_required, get_jwt_identity
from services.game_service import (
    update_game_state,
    update_player_stats,
    reset_player_stats,
    get_room_state,
    get_player_state,
)
import logging

logging.basicConfig(level=logging.INFO)

game_mech_bp = Blueprint('game_mechanics', __name__)

# --- Room State Endpoints ---

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
    """Get the current state of the player (Hunger, Sanity)."""
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
    """Reset the player's stats (Hunger and Sanity)."""
    try:
        reset_state = reset_player_stats(user_id)
        if not reset_state:
            return jsonify({'msg': f'Player with ID {user_id} not found'}), 404
        return jsonify({'msg': 'Player state reset successfully'}), 200
    except Exception as e:
        logging.error(f"Error resetting player state for player {user_id}: {e}")
        return jsonify({'msg': 'Error resetting player state'}), 500
