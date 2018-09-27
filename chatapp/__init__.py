from flask import Flask
from flask_socketio import SocketIO

socketio = SocketIO()

def create_app(debug=False):

    app = Flask(__name__)
    app.debug = debug
    app.config['SECRET_KEY'] = '666'
    #app.config['SQLALCHEMY_DATABASE_URI'] ='postgresql://postgres:postgres@localhost/DBNAME'
    app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql://root@localhost/development'
    from .main import main as main_blueprint
    app.register_blueprint(main_blueprint)

    socketio.init_app(app)
    return app



