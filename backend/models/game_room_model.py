from backend.extensions import db

class GameRoom(db.Model):
    __tablename__ = 'game_room'
    id = db.Column(db.Integer, primary_key=True)
    room_name = db.Column(db.String(80), unique=True, nullable=False)
    is_active = db.Column(db.Boolean, default=True)