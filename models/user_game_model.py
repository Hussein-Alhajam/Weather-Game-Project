from extensions import db

class UserGameRoom(db.Model):

    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), primary_key=True)
    room_id = db.Column(db.Integer, db.ForeignKey('game_room.id'), primary_key=True)
    
    user = db.relationship('User', backref=db.backref('user_game_rooms', lazy=True))
    room = db.relationship('GameRoom', backref=db.backref('user_game_rooms', lazy=True))
