from datetime import datetime
from extensions import db

class PlayerState(db.Model):
    __tablename__ = 'player_state'
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    hunger_level = db.Column(db.Float, default=100.0)
    health_level = db.Column(db.Float, default=100.0)
    stamina_level = db.Column(db.Float, default=100.0)
    last_updated = db.Column(db.DateTime, default=datetime.utcnow)
