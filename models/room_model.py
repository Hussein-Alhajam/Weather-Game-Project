from extensions import db

class GameRoom(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    room_name = db.Column(db.String(80), unique=True, nullable=False)
    is_active = db.Column(db.Boolean, default=True)

    # Relationship with users (many users can belong to a room)
    users = db.relationship('User', backref='game_room', lazy=True)
