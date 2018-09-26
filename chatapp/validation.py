from flask_wtf import Form 
from wtforms import TextField, TextAreaField, SubmitField, validators, ValidationError, PasswordField
from models import db, User, RoomName

class RoomForm(Form):
	roomname = TextField("NameRoom", [validators.Required("Please enter Room Name")])
	submit = SubmitField("Create Room")

	def __init__(self, *args,**kwargs):
		Form.__init__(self, *args,**kwargs)

	def validate(self):
		if not Form.validate(self):
			return False
		topic = RoomName.query.filter_by(topicname = self.roomname.data.lower()).first()
		if topic:
			self.roomname.errors.append("That topic name is already exist")
			return False
		else:
			return True

class RegisterForm(Form):

  	username = TextField("Username",[validators.Required("Please enter your first name.")])
  	email = TextField("Email",  [validators.Required("Please enter your email address.")])
  	password = PasswordField('Password', [validators.Required("Please enter a password.")])
  	submit = SubmitField("Create account")

  	def __init__(self,*args, **kwargs):
  		Form.__init__(self, *args,**kwargs)

  	


class LoginForm(Form):

	def __init__(self, *args, **kwargs):
		Form.__init__(self,*args,**kwargs)

	def validate(self):
		if not Form.validate(self):
			return False
	user = User.query.filter_by(email = self.email.data).first()
	



