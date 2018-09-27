from flask_socketio import SocketIO
from flask_sqlalchemy import SQLAlchemy
from flask import Flask

# resolving ERROR: WebSocket transport not available. Install gevent for imporved perfomance
from gevent import monkey
monkey.patch_all()

db = SQLAlchemy()
socketio = SocketIO()

app = Flask(__name__)
app.config['SECRET_KEY'] = '666'
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://postgres:postgres@localhost/DBNAME'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.debug = True
db = SQLAlchemy(app)
socketio.init_app(app)

