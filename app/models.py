from . import db, login_manager
from flask_login import UserMixin
from datetime import datetime


# -----------------------------
# USER (MSME)
# -----------------------------
class User(db.Model, UserMixin):
    __tablename__ = "users"

    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(120), unique=True, nullable=False)
    name = db.Column(db.String(100), nullable=False)


    company_name = db.Column(db.String(150))
    subscription_plan = db.Column(db.String(50), default="free")


    orders = db.relationship("Order", back_populates="user", lazy=True, cascade="all, delete-orphan")
    


# -----------------------------
# ORDER
# -----------------------------
class Order(db.Model):
    __tablename__ = "orders"

    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    description = db.Column(db.String(255))
    pickup_location = db.Column(db.String(255))
    dropoff_location = db.Column(db.String(255))
    amount = db.Column(db.Float)
    status = db.Column(db.String(50), default="pending")
    created_at = db.Column(db.DateTime, default=datetime.utcnow)


    user = db.relationship("User", back_populates="orders")


# Login Manager
# ----------------------------
@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))
