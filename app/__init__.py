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

    from .models import User, Order, Driver
    return app


def create_db(app):
    with app.app_context():
        db.create_all()
