from flask import Blueprint, request, jsonify
from services.room_service import create_room, join_room, leave_room
from flask_jwt_extended import jwt_required, get_jwt_identity
from flask_socketio import join_room as socket_join_room, leave_room as socket_leave_room, emit
from app import socketio
import logging

logging.basicConfig(level=logging.INFO)

room_bp = Blueprint('room', __name__)

@socketio.on('join')
@jwt_required()
def handle_join(data):
    room = data['room']
    username = get_jwt_identity()
    try:
        socket_join_room(room)
        emit('room_message', {'message': f'{username} has joined the room.'}, room=room)
    except Exception as e:
        logging.error(f"Error in joining room {room}: {e}")
        emit('error', {'message': f'Failed to join room {room}.'})

@socketio.on('leave')
@jwt_required()
def handle_leave(data):
    room = data['room']
    username = get_jwt_identity()
    try:
        socket_leave_room(room)
        emit('room_message', {'message': f'{username} has left the room.'}, room=room)
    except Exception as e:
        logging.error(f"Error in leaving room {room}: {e}")
        emit('error', {'message': f'Failed to leave room {room}.'})

@socketio.on('send_message')
@jwt_required()
def handle_message(data):
    room = data['room']
    message = data['message']
    username = get_jwt_identity()
    try:
        emit('room_message', {'username': username, 'message': message}, room=room)
    except Exception as e:
        logging.error(f"Error sending message to room {room}: {e}")
        emit('error', {'message': f'Failed to send message in room {room}.'})
