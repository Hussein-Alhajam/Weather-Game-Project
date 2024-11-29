from datetime import datetime
from backend.extensions import db

class PlayerState(db.Model):
    __tablename__ = 'player_state'
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    hunger_level = db.Column(db.Float, default=100.0)
    health_level = db.Column(db.Float, default=100.0)
    sanity_level = db.Column(db.Float, default=100.0)
    stamina_level = db.Column(db.Float, default=100.0)
    last_updated = db.Column(db.DateTime, default=datetime.utcnow)

    def to_dict(self):
        return {
            "id": self.id,
            "user_id": self.user_id,
            "hunger_level": self.hunger_level,
            "health_level": self.health_level,
            "stamina_level": self.stamina_level,
            "last_updated": self.last_updated.isoformat() if self.last_updated else None,
        }