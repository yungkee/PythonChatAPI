from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

class User(db.Model):
  uid = db.Column(db.Integer, primary_key = True)
  username = db.Column(db.String(100))
  email = db.Column(db.String(120), unique=True)
  rooms = db.relationship('Room', backref='User', lazy='dynamic')
  messages = db.relationship('Message', backref='User', lazy='dynamic')
  
  def __init__(self, username, email, password):
    self.username = username
    self.email = email.lower()
    self.password = password

class Room(db.Model):
  uid = db.Column(db.Integer, primary_key = True)
  roomname = db.Column(db.String(100), unique=True)
  user_id = db.Column(db.Integer, db.ForeignKey(User.uid))
  messages = db.relationship('Message', backref='Room', lazy='dynamic')

  def __init__(self, roomname, user_id):
    self.roomname = roomname.title()
    self.user_id = user_id

class Message(db.Model):
  uid = db.Column(db.Integer, primary_key = True)
  text = db.Column(db.String(4096))
  user_id = db.Column(db.Integer, db.ForeignKey(User.uid))
  room_id = db.Column(db.Integer, db.ForeignKey(Room.uid))

  def __init__(self, text, user_id, room_id):
    self.text = text
    self.user_id = user_id
    self.room_id = room_id