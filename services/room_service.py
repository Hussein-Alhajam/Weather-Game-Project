from extensions import db
import logging

logging.basicConfig(level=logging.INFO)

def create_room(room_name):
    try:
        from models.room_model import GameRoom
        new_room = GameRoom(room_name=room_name)
        db.session.add(new_room)
        db.session.commit()
        logging.info(f"Room {room_name} created successfully.")
        return new_room
    except Exception as e:
        db.session.rollback()
        logging.error(f"Error creating room {room_name}: {e}")
        return None

def join_room(room_name):
    try:
        from models.room_model import GameRoom
        room = GameRoom.query.get(room_name)
        if room:
            room.is_active = True
            db.session.commit()
            logging.info(f"Room {room_name} joined successfully.")
            return True
        else:
            logging.warning(f"Room {room_name} not found.")
            return False
    except Exception as e:
        db.session.rollback()
        logging.error(f"Error joining room {room_name}: {e}")
        return False

def leave_room(room_name):
    try:
        from models.room_model import GameRoom
        room = GameRoom.query.get(room_name)
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
