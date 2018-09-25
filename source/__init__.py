from flask_socketio import SocketIO
from flask_sqlalchemy import SQLAlchemy
from flask import Flask

socketio = SocketIO()
db = SQLAlchemy()

def create_app(debug=True):
    app = Flask(__name__)
    app.config['SECRET_KEY'] = '666'
    app.debug = debug
    db.init_app(app)
    socketio.init_app(app)
    
    return app

            