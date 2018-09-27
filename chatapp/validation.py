from flask_wtf import Form 
from wtforms import TextField, TextAreaField, SubmitField, validators, ValidationError, PasswordField
from models import db, User, Room


class RoomForm(Form):
	roomname = TextField("Room", [validators.Required("Please enter the name of the room")])
	submit = SubmitField("Create Room")

	# def __init__(self, *args,**kwargs):
	# 	Form.__init__(self, *args,**kwargs)

	def validate(self):
		if not Form.validate(self):
			return False

		room = Room.query.filter_by(roomname = self.roomname.data.lower()).first()
		if room:
			self.roomname.errors.append("That room name is already taken")
			return False
		else:
			return True

class RegisterForm(Form):
  	username = TextField("Username",[validators.Required("Please enter your first name.")])
  	email = TextField("Email",  [validators.Required("Please enter your email address.")])
  	password = PasswordField('Password', [validators.Required("Please enter a password.")])
  	submit = SubmitField("Create account")

  	# def __init__(self,*args, **kwargs):
  	# 	Form.__init__(self, *args,**kwargs)

  	def validate(self):
  		if not Form.validate(self):
  			return False

  		user = User.query.filter_by(email= self.email.data.lower()).first()
  		if user:
  			self.errors.append("Invalid e-mail or password")
  			return False
  		else:
  			return True

class LoginForm(Form):
	email = TextField("Email", [validators.Required("Please enter your email address."), validators.Email("Please enter your email address")])
	password = PasswordField("Password",[validators.Required("Please enter a password")])
	submit = SubmitField("LogIn")

	# def __init__(self, *args, **kwargs):
	# 	Form.__init__(self,*args,**kwargs)

	def validate(self):
		if not Form.validate(self):
			return False
		user = User.query.filter_by(email = self.email.data).first()
		if user:
			return True
		else:
			self.email.errors.append("Invalid email or password")
			return False



