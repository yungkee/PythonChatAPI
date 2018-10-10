from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

db = SQLAlchemy()

class User(db.Model):
  uid = db.Column(db.Integer, primary_key = True)
  username = db.Column(db.String(100))
  email = db.Column(db.String(120), unique=True)
  topics = db.relationship('Topic', backref='User', lazy='dynamic')
  messages = db.relationship('Message', backref='User', lazy='dynamic')
  topic_name = db.Column(db.String(100))
  
  def __init__(self, username, email, password):
    self.username = username.title()
    self.email = email.lower()
    self.password = password

  def __str__(self):
    return str(self.uid) + "_" + str(self.username) + "_" + str(self.email) +  "_" + str(self.messages)
    
class BannedUser(db.Model):
  id = db.Column(db.Integer, primary_key = True)
  user_id = db.Column(db.Integer, db.ForeignKey('user.uid'))
  topic_id = db.Column(db.Integer, db.ForeignKey('topic.uid'))
  times_flagged  = db.Column(db.Integer)

  def __init__(self, user_id, topic_id):
    self.user_id = user_id
    self.topic_id = topic_id
    self.times_flagged = 0

class Admin(db.Model):
  id = db.Column(db.Integer, primary_key = True)
  user_id = db.Column(db.Integer, db.ForeignKey('user.uid'))
  topic_id = db.Column(db.Integer, db.ForeignKey('topic.uid'))

  def __init__(self, user_id, topic_id):
    self.user_id = user_id
    self.topic_id = topic_id

class Topic(db.Model):
  uid = db.Column(db.Integer, primary_key = True)
  topicname = db.Column(db.String(100), unique=True)
  user_id = db.Column(db.Integer, db.ForeignKey(User.uid))
  messages = db.relationship('Message', backref='Topic', lazy='dynamic')

  def __init__(self, topicname, user_id):
    self.topicname = topicname.title()
    self.user_id = user_id

class Message(db.Model):
  uid = db.Column(db.Integer, primary_key = True)
  text = db.Column(db.String(4096))
  posted = db.Column(db.DateTime, default = datetime.now)
  user_id = db.Column(db.Integer, db.ForeignKey(User.uid))
  user_email = db.Column(db.String(128))
  topic_id = db.Column(db.Integer, db.ForeignKey(Topic.uid))
  topic_name = db.Column(db.String(100))

  def __init__(self, text, user_id, user_email, topic_id, topic):
    self.text = text
    self.user_id = user_id
    self.user_email = user_email
    self.topic_id = topic_id
    self.topic_name = topic