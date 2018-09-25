from flask_wtf import Form 
from wtforms import TextField, TextAreaField, SubmitField, validators, ValidationError, PasswordField
from models import db, User, Topic

class MainForm(Form):
	topicname = TextField("Topic", [validators.Required("Please enter Room Name")])

	def __init__(self, *args,**kwargs):
		Form.__init__(self, *args,**kwargs)

	def validate(self):
		if not Form.validate(self):
			return False
		topic = Topic.query.filter_by(topicname = self.topicname.data.lower()).first()
		if topic:
			self.topicname.errors.append("That topic name is already taken")
			return False
		else:
			return True

class RegistrationForm(Form):
  email = TextField("Email",  [validators.Required("Please enter your email address.")])
  password = PasswordField('Password', [validators.Required("Please enter a password.")])
  submit = SubmitField("Create account")

  def __init__(self, *args, **kwargs):
    Form.__init__(self, *args, **kwargs)
    
    user = User.query.filter_by(email = self.email.data.lower()).first()
    if user:
      self.email.errors.append("That email is already taken")
      return False
    else:
      return True