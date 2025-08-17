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
    user_id = db.Column(db.Integer, db.ForeignKey("users.id"), nullable=False)

    # Pickup & Delivery
    pickup_address = db.Column(db.String(200), nullable=False)
    delivery_address = db.Column(db.String(200), nullable=False)
    supplier_name = db.Column(db.String(100))
    supplier_phone = db.Column(db.String(15))
    customer_name = db.Column(db.String(100))
    customer_phone = db.Column(db.String(15))

    # Package Details
    package_name = db.Column(db.String(100), nullable=False)
    package_priority = db.Column(db.String(20), nullable=False)
    quantity = db.Column(db.Integer, nullable=False)
    package_type = db.Column(db.String(50), nullable=False)
    package_description = db.Column(db.String(300))

    # Logistics
    logistic_company = db.Column(db.String(100), nullable=False)
    driver_id = db.Column(db.Integer, db.ForeignKey("drivers.id"))

    # Schedule
    date = db.Column(db.Date, nullable=False)
    time_slot = db.Column(db.Time, nullable=False)

    created_at = db.Column(db.DateTime, default=datetime.now)

    # Relationship
    driver = db.relationship("Driver", back_populates="orders")
    user = db.relationship("User", back_populates="orders")


class Driver(db.Model):
    __tablename__ = "drivers"
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    phone = db.Column(db.String(15), nullable=False)
    truck_no = db.Column(db.String(50), nullable=True)

    # Relationship with Order
    orders = db.relationship("Order", back_populates="driver")




# Login Manager
# ----------------------------
@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))
