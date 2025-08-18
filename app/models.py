from . import db, login_manager
from flask_login import UserMixin
from datetime import datetime


# -----------------------------
# WAREHOUSE
# -----------------------------
class Warehouse(db.Model):
    __tablename__ = "warehouses"
    
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    address = db.Column(db.String(200), nullable=False)
    city = db.Column(db.String(100), nullable=False)
    state = db.Column(db.String(100), nullable=False)
    pincode = db.Column(db.String(10), nullable=False)
    contact_person = db.Column(db.String(100))
    contact_phone = db.Column(db.String(15))
    is_active = db.Column(db.Boolean, default=True)
    created_at = db.Column(db.DateTime, default=datetime.now)
    
    # Foreign key to user
    user_id = db.Column(db.Integer, db.ForeignKey("users.id"), nullable=False)
    
    # Relationships
    user = db.relationship("User", back_populates="warehouses", foreign_keys=[user_id])
    orders = db.relationship("Order", back_populates="warehouse")


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
    current_warehouse_id = db.Column(db.Integer, db.ForeignKey("warehouses.id"), nullable=True)

    # Relationships
    warehouses = db.relationship("Warehouse", back_populates="user", lazy=True, cascade="all, delete-orphan", foreign_keys=[Warehouse.user_id])
    orders = db.relationship("Order", back_populates="user", lazy=True, cascade="all, delete-orphan")
    current_warehouse = db.relationship("Warehouse", foreign_keys=[current_warehouse_id])


# -----------------------------
# ORDER
# -----------------------------
class Order(db.Model):
    __tablename__ = "orders"
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey("users.id"), nullable=False)
    warehouse_id = db.Column(db.Integer, db.ForeignKey("warehouses.id"), nullable=False)

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
    time_slot = db.Column(db.String(20), nullable=False)  # Changed from Time to String

    created_at = db.Column(db.DateTime, default=datetime.now)

    # Relationships
    driver = db.relationship("Driver", back_populates="orders")
    user = db.relationship("User", back_populates="orders")
    warehouse = db.relationship("Warehouse", back_populates="orders")


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
