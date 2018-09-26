from flask_socketio import SocketIO
from flask_sqlalchemy import SQLAlchemy
from flask import Flask

db = SQLAlchemy()
socketio = SocketIO()

app = Flask(__name__)
app.config['SECRET_KEY'] = '666'
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://postgres:postgres@localhost/DBNAME'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.debug = True
db = SQLAlchemy(app)
from chatapp.models import models as data_base_blueprint
app.register_blueprint(data_base_blueprint)
socketio.init_app(app)