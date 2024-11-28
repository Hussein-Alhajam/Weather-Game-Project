from datetime import datetime, timedelta
import logging
import random
from extensions import db, socketio
from models.Inventory import Inventory
from models.game_state import GameRoomState
from models.player_state import PlayerState
from models.game_room_model import GameRoom
from models.resource import Resource
from models.save_game import SavedGame
from services.weather_service import get_weather_for_location, get_location_from_ip


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
    player_state = PlayerState.query.filter_by(user_id=user_id).first()
    if not player_state:
        logging.error(f"Player state for player ID {user_id} not found.")
        return None

    elapsed_minutes = (datetime.utcnow() - player_state.last_updated).total_seconds() / 60

    # Decrease hunger level
    hunger_decrease_rate = 1  # Placeholder, adjust as necessary
    player_state.hunger_level = max(0, player_state.hunger_level - (elapsed_minutes * hunger_decrease_rate))

    # Decrease sanity level based on time of day
    game_state = GameRoomState.query.filter_by(room_id=player_state.room_id).first()
    if not game_state:
        logging.error(f"Game room state for room ID {player_state.room_id} not found.")
        return None

    time_of_day = get_time_of_day(game_state)
    if time_of_day == "Day":
        sanity_decrease_rate = 0.5  # Slower during the day
    else:
        sanity_decrease_rate = 1.0  # Faster at night

    player_state.sanity_level = max(0, player_state.sanity_level - (elapsed_minutes * sanity_decrease_rate))

    # Update last_updated
    player_state.last_updated = datetime.utcnow()
    db.session.commit()

    # Notify client of updated stats
    socketio.emit('player_update', {
        'user_id': user_id,
        'hunger': player_state.hunger_level,
        'health': player_state.health_level,
        'sanity': player_state.sanity_level,
    }, room=str(player_state.room_id))

    return player_state


def reset_player_stats(user_id):
    player_state = PlayerState.query.filter_by(user_id=user_id).first()
    if not player_state:
        logging.error(f"Player state for player ID {user_id} not found.")
        return None

    # Reset stats to default values
    player_state.hunger_level = 100.0
    player_state.health_level = 100.0
    player_state.sanity_level = 100.0
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
    player_state = PlayerState.query.filter_by(user_id=user_id).first()
    if not player_state:
        logging.error(f"Player state for player ID {user_id} not found.")
        return None

    return {
        'user_id': player_state.id,
        'hunger': player_state.hunger_level,
        'health': player_state.health_level,
        'sanity': player_state.sanity_level,
        'last_updated': player_state.last_updated
    }

def apply_weather_effects(player_state, weather_data):
    condition = weather_data.get("condition", {}).get("text", "Clear")
    effects = {
        "Clear": {"visibility": 1.0, "stamina_usage": 1.0},
        "Rain": {"visibility": 0.8, "stamina_usage": 1.1},
        "Snow": {"health_loss": 0.5, "stamina_usage": 1.2},
        "Thunderstorm": {"health_loss_chance": 0.1, "visibility": 0.7},
    }.get(condition, {})

    player_state.visibility = effects.get("visibility", 1.0)
    player_state.stamina_level -= effects.get("health_loss", 0)
    player_state.stamina_usage_rate = effects.get("stamina_usage", 1.0)

    if condition == "Thunderstorm" and random.random() < effects.get("health_loss_chance", 0):
        player_state.health_level -= 10

    player_state.health_level = max(0, player_state.health_level)
    player_state.stamina_level = max(0, player_state.stamina_level)
    db.session.commit()


def update_gameplay_weather(user_ip):
    lat, lon = get_location_from_ip(user_ip)
    if not lat or not lon:
        logging.error(f"Could not get location for IP {user_ip}")
        return None

    weather_data = get_weather_for_location(lat, lon)
    if not weather_data:
        logging.error("Failed to retrieve weather data.")
        return None

    players = PlayerState.query.all()
    for player in players:
        apply_weather_effects(player, weather_data)

    socketio.emit('weather_update', {
        "weather": weather_data
    })

    return weather_data  # Return weather data for use in the endpoint


def initialize_game_room(room_id, players, initial_resources, initial_inventory):
    try:
        if not players:
            raise ValueError("Players list is empty or not provided")

        logging.info(f"Initializing game room {room_id} with players: {players}")

        # Add game room state
        game_room_state = GameRoomState(
            room_id=room_id,
            current_state="Day",
            last_transition=datetime.utcnow(),
            cycle_duration=15
        )
        db.session.add(game_room_state)

        # Initialize player states and inventory
        for player in players:
            user_id = player.get("user_id")
            if not user_id:
                logging.error(f"Player entry is missing 'user_id': {player}")
                continue  # Skip invalid player entries

            existing_player_state = PlayerState.query.filter_by(user_id=user_id).first()
            if existing_player_state:
                logging.warning(f"PlayerState already exists for user {user_id}")
                continue  # Avoid duplicate entries

            player_state = PlayerState(
                user_id=user_id,
                hunger_level=100.0,
                health_level=100.0,
                sanity_level=100.0,
                last_updated=datetime.utcnow()
            )
            db.session.add(player_state)
            logging.info(f"PlayerState created for user {user_id}")

            # Add inventory items
            for item in initial_inventory.get(user_id, []):
                inventory_item = Inventory(
                    user_id=user_id,
                    item_name=item["item_name"],
                    quantity=item["quantity"]
                )
                db.session.add(inventory_item)

        db.session.commit()
        logging.info(f"Game room {room_id} initialized successfully")
        return {"msg": "Game room initialized successfully."}
    except Exception as e:
        db.session.rollback()
        logging.error(f"Error initializing game room: {e}")
        raise

    
def save_game(user_id):
    try:
        logging.info(f"Attempting to save game for user {user_id}")

        # Fetch game state for the user
        player_states = PlayerState.query.filter_by(user_id=user_id).all()
        inventory = Inventory.query.filter_by(user_id=user_id).all()
        resources = Resource.query.all()  # Shared for all users in the room
        game_room_state = GameRoomState.query.all()

        # Log detailed debug information
        logging.info(f"Player states for user {user_id}: {player_states}")
        if not player_states:
            logging.error(f"No PlayerState found for user {user_id}")

        logging.info(f"Inventory for user {user_id}: {inventory}")
        if not inventory:
            logging.warning(f"Inventory is empty for user {user_id}, but this may not be critical.")

        logging.info(f"Resources in the game room: {resources}")
        if not resources:
            logging.warning("No resources found in the game room, but this may not be critical.")

        logging.info(f"Game room state: {game_room_state}")
        if not game_room_state:
            logging.error("No GameRoomState found.")

        if not player_states:
            logging.warning(f"No PlayerState found for user {user_id}. Proceeding without it.")

        if not game_room_state:
            logging.warning("No GameRoomState found. Proceeding without it.")


        # Serialize data
        saved_game = SavedGame(
            user_id=user_id,
            game_room_state=[room_state.to_dict() for room_state in game_room_state],
            player_states=[player_state.to_dict() for player_state in player_states],
            inventory=[inv.to_dict() for inv in inventory],
            resources=[resource.to_dict() for resource in resources],
        )

        # Save the serialized data to the database
        db.session.add(saved_game)
        db.session.commit()

        logging.info(f"Game state successfully saved for user {user_id}")
        return saved_game

    except Exception as e:
        logging.error(f"Error saving game for user {user_id}: {e}")
        db.session.rollback()
        return None

def load_game(user_id, save_id):
    try:
        # Fetch the saved game
        saved_game = SavedGame.query.filter_by(user_id=user_id, id=save_id).first()
        if not saved_game:
            raise ValueError("Save not found")

        # Restore game room state
        GameRoomState.query.delete()
        for room_state in saved_game.game_room_state:
            room_state['last_transition'] = datetime.fromisoformat(room_state['last_transition'])
            new_state = GameRoomState(**room_state)
            db.session.add(new_state)

        # Restore player states
        PlayerState.query.filter_by(user_id=user_id).delete()
        for player_state in saved_game.player_states:
            new_player_state = PlayerState(**player_state)
            db.session.add(new_player_state)

        # Restore inventory
        Inventory.query.filter_by(user_id=user_id).delete()
        for inv in saved_game.inventory:
            new_inv = Inventory(**inv)
            db.session.add(new_inv)

        # Restore resources (Validate room_id)
        Resource.query.delete()
        for resource in saved_game.resources:
            if 'room_id' not in resource or resource['room_id'] is None:
                logging.error(f"Missing room_id for resource: {resource}")
                continue  # Skip this resource
            new_resource = Resource(**resource)
            db.session.add(new_resource)

        db.session.commit()
        return saved_game
    except Exception as e:
        logging.error(f"Error loading game for user {user_id}: {e}")
        db.session.rollback()
        return None
