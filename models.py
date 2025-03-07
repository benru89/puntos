import datetime
from app import db

class Player(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    # Relationship to access the player's training points
    points = db.relationship('TrainingPoints', backref='player', lazy=True)

class TrainingPoints(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    player_id = db.Column(db.Integer, db.ForeignKey('player.id'), nullable=False)
    date = db.Column(db.Date, default=datetime.date.today)
    points = db.Column(db.Integer, nullable=False)
