from datetime import datetime, timedelta
import logging
from extensions import db, socketio
from models.game_state import GameRoomState
from models.player_state import PlayerState
from models.game_room_model import GameRoom

# Helper Functions
def get_time_of_day(game_room_state):
    elapsed = datetime.utcnow() - game_room_state.last_transition
    # Use cycle_duration in GameRoomState to determine the length of each day/night cycle
    day_duration = timedelta(minutes=game_room_state.cycle_duration)
    night_duration = timedelta(minutes=game_room_state.cycle_duration // 2)
    total_cycle_duration = day_duration + night_duration
    cycle_position = elapsed % total_cycle_duration

    if cycle_position < day_duration:
        return "Day"
    return "Night"


def update_game_state(room_id):
    game_state = GameRoomState.query.filter_by(room_id=room_id).first()
    if not game_state:
        logging.error(f"Game room state for room {room_id} not found.")
        return None

    current_time_of_day = get_time_of_day(game_state)

    # Update state if it has changed
    if current_time_of_day != game_state.current_state:
        game_state.current_state = current_time_of_day
        game_state.last_transition = datetime.utcnow()
        db.session.commit()

        # Notify clients about the state change
        socketio.emit('state_change', {
            'room_id': room_id,
            'new_state': current_time_of_day
        }, room=str(room_id))

    return current_time_of_day


def update_player_stats(user_id):
    player_state = PlayerState.query.filter_by(id=user_id).first()
    if not player_state:
        logging.error(f"Player state for player ID {user_id} not found.")
        return None

    elapsed_minutes = (datetime.utcnow() - player_state.last_updated).total_seconds() / 60

    # Decrease hunger
    hunger_decrease_rate = 1  # Placeholder, you can adjust this based on room conditions or other events
    player_state.hunger_level = max(0, player_state.hunger_level - (elapsed_minutes * hunger_decrease_rate))

    # Decrease sanity based on time of day
    game_state = GameRoomState.query.filter_by(room_id=player_state.room_id).first()
    if not game_state:
        logging.error(f"Game room state for room ID {player_state.room_id} not found.")
        return None

    time_of_day = get_time_of_day(game_state)
    if time_of_day == "Day":
        sanity_decrease_rate = 0.5  # Decrease slower during the day
    else:
        sanity_decrease_rate = 1.0  # Decrease faster at night

    player_state.sanity_level = max(0, player_state.sanity_level - (elapsed_minutes * sanity_decrease_rate))

    # Update the last_updated time
    player_state.last_updated = datetime.utcnow()
    db.session.commit()

    # Notify client of updated stats
    socketio.emit('player_update', {
        'user_id': user_id,
        'hunger': player_state.hunger_level,
        'sanity': player_state.sanity_level
    }, room=str(player_state.room_id))

    return player_state


def reset_player_stats(user_id):
    player_state = PlayerState.query.filter_by(id=user_id).first()
    if not player_state:
        logging.error(f"Player state for player ID {user_id} not found.")
        return None

    # Reset stats to default values
    player_state.hunger_level = 100.0
    player_state.health_level = 100.0
    player_state.stamina_level = 100.0
    player_state.last_updated = datetime.utcnow()
    db.session.commit()

    return player_state


def get_room_state(room_id):
    try:
        room_state = GameRoomState.query.filter_by(room_id=room_id).first()
        if not room_state:
            logging.error(f"Room state for room ID {room_id} not found.")
            return None
        return {
            "room_id": room_state.room_id,
            "state": room_state.current_state,
            "last_updated": room_state.last_transition
        }
    except Exception as e:
        logging.error(f"Error fetching room state for room {room_id}: {e}")
        return None


def get_player_state(user_id):
    player_state = PlayerState.query.filter_by(id=user_id).first()
    if not player_state:
        logging.error(f"Player state for player ID {user_id} not found.")
        return None

    return {
        'user_id': player_state.id,
        'hunger': player_state.hunger_level,
        'health': player_state.health_level,
        'stamina': player_state.stamina_level,
        'last_updated': player_state.last_updated
    }
