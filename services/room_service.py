from datetime import datetime
from extensions import db
import logging

from models.game_room_model import GameRoom
from models.game_state import GameRoomState
from models.player_state import PlayerState
from models.user_model import User

logging.basicConfig(level=logging.INFO)

def create_room(room_name):
    try:
        # Create a new game room
        new_room = GameRoom(room_name=room_name)
        db.session.add(new_room)
        db.session.commit()

        # Create a game room state entry for this room
        new_game_state = GameRoomState(
            room_id=new_room.id,
            last_transition=datetime.utcnow(),
            current_state="Day"
        )
        db.session.add(new_game_state)
        db.session.commit()

        logging.info(f"Room {room_name} created successfully.")
        return new_room
    except Exception as e:
        db.session.rollback()
        logging.error(f"Error creating room {room_name}: {e}")
        return None


def join_room(room_name, username):
    try:
        # Fetch the game room
        room = GameRoom.query.filter_by(room_name=room_name).first()
        if not room:
            logging.warning(f"Room '{room_name}' not found.")
            return False

        # Fetch user by username
        user = User.query.filter_by(username=username).first()
        if not user:
            logging.warning(f"User '{username}' not found.")
            return False

        # Create a player state for this user if it doesn't exist
        player_state = PlayerState.query.filter_by(user_id=user.id).first()
        if not player_state:
            new_player_state = PlayerState(
                user_id=user.id,
                hunger_level=100,
                health_level=100,
                stamina_level=100,
                last_updated=datetime.utcnow()
            )
            db.session.add(new_player_state)
            db.session.commit()

        logging.info(f"User '{username}' joined room '{room_name}' successfully.")
        return True
    except Exception as e:
        db.session.rollback()
        logging.error(f"Error joining room '{room_name}' for user '{username}': {e}")
        return False


def leave_room(room_name):
    try:
        from models.game_room_model import GameRoom
        room = GameRoom.query.filter_by(room_name=room_name).first()
        if room:
            room.is_active = False
            db.session.commit()
            logging.info(f"Room {room_name} left successfully.")
            return True
        else:
            logging.warning(f"Room {room_name} not found.")
            return False
    except Exception as e:
        db.session.rollback()
        logging.error(f"Error leaving room {room_name}: {e}")
        return False
