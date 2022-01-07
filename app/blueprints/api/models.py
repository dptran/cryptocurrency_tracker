from app import db
from datetime import datetime as dt

class Tracker(db.Model):
    id = db.Column(db.String, primary_key=True)
    name = db.Column(db.String, nullable=False)
    symbol = db.Column(db.String)
    rank = db.Column(db.Integer)
    price = db.Column(db.Float)
    volume = db.Column(db.Float)
    marketCap = db.Column(db.Float)
    availableSupply = db.Column(db.Float)
    totalSupply = db.Column(db.Float)
    priceChange1h = db.Column(db.Float)
    priceChange1d = db.Column(db.Float)
    priceChange1w = db.Column(db.Float)
    date_created = db.Column(db.DateTime, default=dt.utcnow)
    owner = db.Column(db.Integer, db.ForeignKey('user.id'))

    def to_dict(self):
        from app.blueprints.auth.models import User

        data = {
            'name': self.name,
            'description': self.description,
            'date_created': self.date_created,
            'owner': User.query.get(self.owner).to_dict(),
            'body': self.body,
            'date_created': self.date_created,
            'user': User.query.get(self.user_id).to_dict()
        }
        return data