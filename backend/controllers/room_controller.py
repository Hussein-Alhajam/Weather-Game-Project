from datetime import timedelta
from flask import Blueprint, request, jsonify
from services.room_service import create_room, join_room, leave_room
from flask_jwt_extended import create_access_token, jwt_required, get_jwt_identity
from flask_socketio import join_room as socket_join_room, leave_room as socket_leave_room, emit
from backend.extensions import socketio
import logging

logging.basicConfig(level=logging.INFO)

room_bp = Blueprint('room', __name__)

# --- HTTP Endpoints ---

@room_bp.route('/create', methods=['POST'])
@jwt_required()
def create():
    """Endpoint to create a new room."""
    data = request.get_json()

    # Validate incoming data
    if not data or 'room_name' not in data:
        return jsonify({'msg': 'Room name is required'}), 400

    room_name = data.get('room_name')
    if not isinstance(room_name, str) or not room_name.strip():
        return jsonify({'msg': 'Room name must be a non-empty string'}), 400

    username = get_jwt_identity()
    try:
        room = create_room(room_name)
        if room is None:
            raise Exception("Room creation failed.")
        return jsonify({'msg': f"Room '{room_name}' created successfully", 'room_id': room.id}), 201
    except Exception as e:
        logging.error(f"Error creating room: {e}")
        return jsonify({'msg': 'Error creating room'}), 500

@room_bp.route('/join', methods=['POST'])
@jwt_required()
def join():
    """Endpoint to join a room."""
    data = request.get_json()

    # Validate incoming data
    if not data or 'room_name' not in data or 'username' not in data:
        return jsonify({'msg': 'Room name and username are required'}), 400

    room_name = data.get('room_name')
    username = data.get('username')

    # Validate room name and username
    if not isinstance(room_name, str) or not room_name.strip():
        return jsonify({'msg': 'Room name must be a non-empty string'}), 400
    if not isinstance(username, str) or not username.strip():
        return jsonify({'msg': 'Username must be a non-empty string'}), 400

    try:
        if not join_room(room_name, username):
            raise Exception(f"Room '{room_name}' not found or join failed.")
        return jsonify({'msg': f"{username} joined room '{room_name}'"}), 200
    except Exception as e:
        logging.error(f"Error joining room '{room_name}' for user '{username}': {e}")
        return jsonify({'msg': 'Error joining room'}), 500


@room_bp.route('/leave', methods=['POST'])
@jwt_required()
def leave():
    """Endpoint to leave a room."""
    data = request.get_json()

    # Validate incoming data
    if not data or 'room_name' not in data:
        return jsonify({'msg': 'Room name is required'}), 400

    room_name = data.get('room_name')
    if not isinstance(room_name, str) or not room_name.strip():
        return jsonify({'msg': 'Room name must be a non-empty string'}), 400

    username = get_jwt_identity()
    try:
        if not leave_room(room_name):
            raise Exception(f"Room '{room_name}' not found or leave failed.")
        return jsonify({'msg': f"{username} left room '{room_name}'"}), 200
    except Exception as e:
        logging.error(f"Error leaving room '{room_name}': {e}")
        return jsonify({'msg': 'Error leaving room'}), 500

# --- Socket.IO Events ---

@socketio.on('join')
@jwt_required()
def handle_join(data):
    """Socket.IO event to handle a user joining a room."""
    room = data.get('room')
    username = get_jwt_identity()

    if not room or not isinstance(room, str) or not room.strip():
        emit('error', {'message': 'Room name must be a non-empty string'})
        return

    try:
        socket_join_room(room)
        emit('room_message', {'message': f'{username} has joined the room.'}, room=room)
    except Exception as e:
        logging.error(f"Error in joining room {room}: {e}")
        emit('error', {'message': f'Failed to join room {room}.'})

@socketio.on('leave')
@jwt_required()
def handle_leave(data):
    """Socket.IO event to handle a user leaving a room."""
    room = data.get('room')
    username = get_jwt_identity()

    if not room or not isinstance(room, str) or not room.strip():
        emit('error', {'message': 'Room name must be a non-empty string'})
        return

    try:
        socket_leave_room(room)
        emit('room_message', {'message': f'{username} has left the room.'}, room=room)
    except Exception as e:
        logging.error(f"Error in leaving room {room}: {e}")
        emit('error', {'message': f'Failed to leave room {room}.'})

@socketio.on('send_message')
@jwt_required()
def handle_message(data):
    """Socket.IO event to handle sending a message in a room."""
    room = data.get('room')
    message = data.get('message')
    username = get_jwt_identity()

    if not room or not isinstance(room, str) or not room.strip():
        emit('error', {'message': 'Room name must be a non-empty string'})
        return

    if not message or not isinstance(message, str) or not message.strip():
        emit('error', {'message': 'Message must be a non-empty string'})
        return

    try:
        emit('room_message', {'username': username, 'message': message}, room=room)
    except Exception as e:
        logging.error(f"Error sending message to room {room}: {e}")
        emit('error', {'message': f'Failed to send message in room {room}.'})
        
#refresh token
@socketio.on("user_action")
@jwt_required()
def handle_user_action(data):
    identity = get_jwt_identity()
    # Refresh token logic
    new_token = create_access_token(
        identity=identity,
        additional_claims={"user_id": identity},
        expires_delta=timedelta(hours=1)
    )
    emit("token_refresh", {"token": new_token})

