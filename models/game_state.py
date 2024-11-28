from datetime import datetime
from extensions import db

class GameRoomState(db.Model):
    __tablename__ = 'game_room_state'
    id = db.Column(db.Integer, primary_key=True)
    room_id = db.Column(db.Integer, db.ForeignKey('game_room.id'), nullable=False)
    last_transition = db.Column(db.DateTime, default=datetime.utcnow)
    current_state = db.Column(db.String(20), default="Day")  # "Day" or "Night"
    cycle_duration = db.Column(db.Integer, default=15)  # Total cycle in minutes
