from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

class User(db.Model):
    uid = db.Column(db.Integer, primary_key = True)
    username = db.Column(db.String(100), unique = True)
    email = db.Column(db.String(120))

    def __init__(self, username, email, password):
        self.username = username
        self.email =  email.lower()
        self.password = password

class Room(db.Model):
    uid = db.Column(db.Integer, primary_key=True)
    roomname = db.Column(db.String(100), unique=True)
    user_id = db.Column(db.Integer, db.ForeignKey(User.uid))
    
    def __init__(self, roomname, user_id):
        self.roomname = roomname.tilte()
        self.user_id = user_id

class Message(db.Model):
    uid = db.Column(db.Integer, primary_key=True)
    message = db.Column(db.String(4096))
    user_id = db.Column(db.Integer, db.ForeignKey(User.uid))
    room_id = db.Column(db.Integer, db.ForeignKey(Room.uid))

    def __init__(self, message, user_id, room_id):
        self.message = message
        self.user_id = user_id
        self.room_id = room_id