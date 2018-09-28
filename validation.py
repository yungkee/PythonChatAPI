from flask_wtf import Form
from wtforms import TextField, TextAreaField, SubmitField, validators, ValidationError, PasswordField
from models import db, User, Room

class RoomForm(Form):
  roomname = TextField("Room",  [validators.Required("Please enter a room name.")])
  submit = SubmitField("Create chatroom")

  def validate(self):
    if not Form.validate(self):
      return False
    return True
    
    # room = Room.query.filter_by(roomname = self.roomname.data.lower()).first()
    # if room:
    #   self.roomname.errors.append("That room name is already exist")
    #   return False
    # else:
    #   return True

class RegisterForm(Form):
  username = TextField("Username",  [validators.Required("Please enter your username.")])
  email = TextField("Email",  [validators.Required("Please enter your email address."), validators.Email("Please enter your email address.")])
  password = PasswordField('Password', [validators.Required("Please enter a password.")])
  submit = SubmitField("Create account")

  def validate(self):

    if not Form.validate(self):
      return False
    return True
    # user = User.query.filter_by(email = self.email.data.lower()).first()
    # if user:
    #   self.email.errors.append("That email is already exist")
    #   return False
    # else:
    #   return True

class LoginForm(Form):
  email = TextField("Email",  [validators.Required("Please enter your email address."), validators.Email("Please enter your email address.")])
  password = PasswordField('Password', [validators.Required("Please enter a password.")])
  submit = SubmitField("Login")
  

  def validate(self):
    if not Form.validate(self):
      return False
    return True
    
    # user = User.query.filter_by(email = self.email.data).first()
    # if user and user.check_password(self.password.data):
    #   return True
    # else:
    #   self.email.errors.append("Invalid e-mail or password")
    #   return False
