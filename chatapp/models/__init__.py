from flask import Blueprint

models = Blueprint('models', __name__)

from chatapp.models import user, message, room