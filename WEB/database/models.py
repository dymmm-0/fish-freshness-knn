from datetime import datetime

from . import db


class PredictionHistory(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    filename = db.Column(db.String(255), nullable=False)
    predicted_label = db.Column(db.String(50), nullable=False)
    mean_r = db.Column(db.Float, nullable=False)
    mean_g = db.Column(db.Float, nullable=False)
    mean_b = db.Column(db.Float, nullable=False)
    mean_h = db.Column(db.Float, nullable=False)
    mean_s = db.Column(db.Float, nullable=False)
    mean_v = db.Column(db.Float, nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow, nullable=False)
