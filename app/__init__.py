from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from authlib.integrations.flask_client import OAuth
from flask_login import LoginManager

db = SQLAlchemy()
oauth = OAuth()
login_manager = LoginManager()

def create_app():
    app = Flask(__name__)
    app.config.from_object('config.Config')

    db.init_app(app)
    oauth.init_app(app)
    login_manager.init_app(app)

    login_manager.login_view = 'auth.login'

    from .routes.auth import auth
    app.register_blueprint(auth)

    from .routes.views import views
    app.register_blueprint(views)

    from .routes.drivers import drivers
    app.register_blueprint(drivers,url_prefix='/drivers')

    from .routes.msme import msme
    app.register_blueprint(msme,url_prefix='/msme')

    create_db(app)

    from .models import User, Order, Driver, Warehouse
    return app


def create_db(app):
    with app.app_context():
        # Create all tables
        db.create_all()
        
        # Check if we need to migrate existing orders
        migrate_existing_orders(app)


def migrate_existing_orders(app):
    """Migrate existing orders to include warehouse information"""
    from .models import Order, User
    
    # Check if there are orders without warehouse_id
    orders_without_warehouse = Order.query.filter_by(warehouse_id=None).all()
    
    if orders_without_warehouse:
        print(f"Found {len(orders_without_warehouse)} orders without warehouse. Creating default warehouse...")
        
        # Get the first user (assuming there's at least one)
        first_user = User.query.first()
        
        if first_user:
            # Create a default warehouse for the user
            default_warehouse = Warehouse(
                name="Default Warehouse",
                address="Default Address",
                city="Default City",
                state="Default State",
                pincode="000000",
                contact_person=first_user.name,
                contact_phone="N/A",
                is_active=True,
                user_id=first_user.id
            )
            
            db.session.add(default_warehouse)
            db.session.commit()
            
            # Update all existing orders to use the default warehouse
            for order in orders_without_warehouse:
                order.warehouse_id = default_warehouse.id
            
            db.session.commit()
            print("Migration completed successfully!")
        else:
            print("No users found. Cannot create default warehouse.")
