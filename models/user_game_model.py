from extensions import db

class UserGameRoom(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    room_id = db.Column(db.Integer, db.ForeignKey('game_room.id'), nullable=False)
    
    user = db.relationship('User', backref=db.backref('user_game_rooms', lazy=True))
    room = db.relationship('GameRoom', backref=db.backref('user_game_rooms', lazy=True))
