from flask import Flask, jsonify
from models import db, Bakery, BakedGood

app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///app.db"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

db.init_app(app)

# ✅ CREATE TABLES + SEED DATA (REQUIRED FOR TESTS)
with app.app_context():
    db.create_all()

    if not Bakery.query.first():
        bakery = Bakery(name="Seed Bakery")
        db.session.add(bakery)
        db.session.commit()

        baked_goods = [
            BakedGood(name="Cake", price=20.0, bakery_id=bakery.id),
            BakedGood(name="Bread", price=5.0, bakery_id=bakery.id),
            BakedGood(name="Pie", price=15.0, bakery_id=bakery.id),
        ]

        db.session.add_all(baked_goods)
        db.session.commit()


@app.route("/bakeries")
def bakeries():
    bakeries = Bakery.query.all()
    return jsonify([b.to_dict() for b in bakeries])


@app.route("/bakeries/<int:id>")
def bakery_by_id(id):
    bakery = Bakery.query.get_or_404(id)
    return jsonify(bakery.to_dict())


@app.route("/baked_goods/by_price")
def baked_goods_by_price():
    goods = BakedGood.query.order_by(BakedGood.price.desc()).all()
    return jsonify([g.to_dict() for g in goods])


@app.route("/baked_goods/most_expensive")
def most_expensive_baked_good():
    good = BakedGood.query.order_by(BakedGood.price.desc()).first()
    if not good:
        return jsonify({}), 200
    return jsonify(good.to_dict())
