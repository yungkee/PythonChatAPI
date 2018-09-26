from chatapp import db

class User(db.Model):
	id = db.Column(db.Integer, primary_key = True)
	username = db.Column(db.String(100), unique = True)
	email = db.Column(db.String(100))
	room_name = db.Column(db.String(100))