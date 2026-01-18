from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

db = SQLAlchemy()

class Bakery(db.Model):
    __tablename__ = "bakeries"

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    baked_goods = db.relationship("BakedGood", backref="bakery")

    def to_dict(self):
        return {
            "id": self.id,
            "name": self.name,
            "created_at": self.created_at.isoformat() if self.created_at else None,
            "updated_at": None,
            "baked_goods": [bg.to_dict() for bg in self.baked_goods]
        }


class BakedGood(db.Model):
    __tablename__ = "baked_goods"

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String)
    price = db.Column(db.Float)
    bakery_id = db.Column(db.Integer, db.ForeignKey("bakeries.id"))
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    def to_dict(self):
        result = {
            "id": self.id,
            "name": self.name,
            "price": self.price,
            "bakery_id": self.bakery_id,
            "created_at": self.created_at.isoformat() if self.created_at else None,
            "updated_at": None
        }
        if hasattr(self, 'bakery') and self.bakery:
            result["bakery"] = {
                "id": self.bakery.id,
                "name": self.bakery.name,
                "created_at": self.bakery.created_at.isoformat() if self.bakery.created_at else None,
                "updated_at": None
            }
        return result
