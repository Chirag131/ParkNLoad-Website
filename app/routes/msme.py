from flask import Blueprint, render_template, session, redirect, url_for, request
from ..models import User
from .. import db
from flask_login import login_required,current_user

msme = Blueprint('msme', __name__)

@msme.route('/')
@login_required
def home():
    return render_template('msme/dashboard.html')