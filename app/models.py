from . import db, login_manager
from flask_login import UserMixin


class User(db.Model,UserMixin):
    __tablename__ = 'users'

    id = db.Column(db.Integer, primary_key=True)

    name = db.Column(db.String(150), nullable=False)
    email = db.Column(db.String(150), unique=True, nullable=False)
    phone = db.Column(db.String(15), unique=True)





@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))