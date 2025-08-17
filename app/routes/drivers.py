from flask import Blueprint, render_template, session, redirect, url_for, request
from ..models import User
from .. import db


drivers = Blueprint('drivers', __name__)

@drivers.route('/')
def home():
    return render_template('index.html')