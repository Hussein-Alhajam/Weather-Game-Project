from backend.extensions import db

class Resource(db.Model):
    __tablename__ = 'resource'
    id = db.Column(db.Integer, primary_key=True)
    type = db.Column(db.String(80), nullable=False)  # e.g., wood, stone
    quantity = db.Column(db.Integer, default=0)
    location_x = db.Column(db.Float, nullable=True)
    location_y = db.Column(db.Float, nullable=True)
    room_id = db.Column(db.Integer, db.ForeignKey('game_room.id'), nullable=False)

    def to_dict(self):
        return {
            "id": self.id,
            "type": self.type,
            "quantity": self.quantity,
            "location_x": self.location_x,
            "location_y": self.location_y,
            "room_id":self.room_id,
        }