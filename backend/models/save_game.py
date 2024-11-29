from extensions import db

class SavedGame(db.Model):
    __tablename__ = 'saved_game'
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    game_room_state = db.Column(db.JSON, nullable=False)  # Stores serialized game room data
    player_states = db.Column(db.JSON, nullable=False)  # Stores serialized player states
    inventory = db.Column(db.JSON, nullable=False)  # Stores serialized inventory
    resources = db.Column(db.JSON, nullable=False)  # Stores serialized resources
    saved_at = db.Column(db.DateTime, default=db.func.now())  # Timestamp of the save

    def to_dict(self):
        return {
            "id": self.id,
            "user_id": self.user_id,
            "game_room_state": self.game_room_state,  # Already in JSON format
            "player_states": self.player_states,  # Already in JSON format
            "inventory": self.inventory,  # Already in JSON format
            "resources": self.resources,  # Already in JSON format
        }