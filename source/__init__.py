from flask import Flask, render_template
from flask_socketio import SocketIO, send

socketio = SocketIO()

def create_app(debug=True):
    app = Flask(__name__)
    app.config['SECRET_KEY'] = '666'
    app.debug = debug
    socketio.init_app(app)
    return app

            