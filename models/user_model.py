from extensions import db

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    password = db.Column(db.String(120), nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=True)  # Useful for Google OAuth users

    # Foreign key to associate users with a room
    game_room_id = db.Column(db.Integer, db.ForeignKey('game_room.id'), nullable=True)
