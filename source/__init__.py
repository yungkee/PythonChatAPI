from flask_socketio import SocketIO
from flask_sqlalchemy import SQLAlchemy
from flask import Flask
from flask_marshmallow import Marshmallow
from app.config import Config

socketio = SocketIO()
db = SQLAlchemy()
ma = Marshmallow()

def create_app(debug=True):
    app = Flask(__name__)
    app.config['SECRET_KEY'] = '666'
    app.debug = debug
    config.init_app(app)
    db.init_app(app)
    ma_init_app(app)
    socketio.init_app(app)
    
    return app

            