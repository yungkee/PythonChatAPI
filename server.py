from flask import Flask, render_template, session, request
from flask_socketio import SocketIO, emit, join_room, leave_room
from flask import render_template, request, flash, session, url_for, redirect
from validation import RegisterForm, LoginForm, RoomForm
from models import db, User, Topic, Message
import datetime

app = Flask(__name__)
app.debug = True
app.config['SECRET_KEY'] = '6666'
socketio = SocketIO(app)
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql://root@localhost/development'

db.init_app(app)


@app.route('/')
def home():
	return render_template('home.html')

@app.route('/chat', methods=['GET', 'POST'])
def chat():
	form = RoomForm()
	rooms = Topic.query.all()
	users = User.query.all()
	messages = Message.query.all()

	session['room'] = 'MainChat'

	if 'email' not in session:
		return redirect(url_for('login'))

	user = User.query.filter_by(email = session['email']).first()

	if user is None:
		return redirect(url_for('login'))
	else:
		if request.method == 'POST':
			if form.validate() == False:
				return render_template('chat.html', form=form, rooms=rooms, users=users, messages=messages)
			else:
				uid = user.uid
				newroom = Topic(form.topicname.data, uid)
				db.session.add(newroom)
				db.session.commit()
				session['topic'] = newroom.topicname
				return redirect('/chat/' + newroom.topicname)
		
		if request.method == 'GET':
			return render_template('chat.html', form=form, rooms=rooms, users=users, messages=messages)

@app.route('/chat/<chatroom_title>')
def show_chatroom(chatroom_title):
	form = RoomForm()
	rooms = Topic.query.all()
	users = User.query.all()
	messages = Message.query.all()

	room = Topic.query.filter_by(topicname = chatroom_title).first()

	if room is None:
		return redirect(url_for('chat'))

	session['room'] = room.topicname

	if 'email' not in session:
		return redirect(url_for('login'))

	user = User.query.filter_by(email = session['email']).first()

	if user is None:
		return redirect(url_for('login'))
	else:
		if request.method == 'POST':
			if form.validate() == False:
				return render_template('chat.html', form=form, rooms=rooms, users=users, messages=messages)
			else:
				uid = user.uid
				newroom = Topic(form.topicname.data, uid)
				db.session.add(newroom)
				db.session.commit()
				session['room'] = newroom.topicname
				return redirect('/chat/' + newroom.topicname)
		
		if request.method == 'GET':
			return render_template('chat.html', form=form, rooms=rooms, users=users, messages=messages)

@app.route('/register', methods=['GET', 'POST'])
def register():
	form = RegisterForm()

	session['room'] = 'MainChat'

	if 'email' in session:
		return redirect(url_for('chat')) 
	
	if request.method == 'POST':
		if form.validate() == False:
			return render_template('register.html', form=form)
		else:
			newuser = User(form.username.data, form.email.data, form.password.data)
			db.session.add(newuser)
			db.session.commit()
			session['email'] = newuser.email
			return redirect(url_for('chat'))
	
	if request.method == 'GET':
		return render_template('register.html', form=form)

@app.route('/login', methods=['GET', 'POST'])
def login():
	form = LoginForm()

	session['room'] = 'MainChat'

	if 'email' in session:
		return redirect(url_for('chat')) 

	if request.method == 'POST':
		if form.validate() == False:
			return render_template('login.html', form=form)
		else:
			session['email'] = form.email.data
			return redirect(url_for('chat'))

	elif request.method == 'GET':
		return render_template('login.html', form=form)

@app.route('/signout')
def signout():
	if 'email' not in session:
		return redirect(url_for('login'))

	session.pop('email', None)
	session.pop('room', None)
	return redirect(url_for('login'))

@socketio.on('create_room', namespace='/chat')
def create_room(message):
	print("New topic\n")
	print(message)
	print(message['data']['room'])
	emit('update_rooms', {'msg': { 'room': message['data']['room'] }}, broadcast=True)

@socketio.on('joinroom', namespace='/chat')
def joinroom(message):
	print('message =', message)
	room = message['data']['room']
	session['room'] = room
	join_room(room)
	print(session.get('email'))
	print('has joined')
	joinedMessage = {'user': session.get('email'), 'msg': session.get('email') + ' has entered ' + room + '.'}
	emit('status', joinedMessage, room=room)
	user = User.query.filter_by(email=session.get('email')).first()
	user.topic_name = room
	print(user.topic_name)
	print(session['room'])
	db.session.commit()


@socketio.on('message', namespace='/chat')
def chat_message(message):
	print("message = ", message)
	print(message['data']['message'])
	email = session.get('email')
	room = session.get('room')
	sendMessage = {'text': message['data']['message'], 'author': email}
	emit('message', sendMessage , room=room)
	user = User.query.filter_by(email=email).first()
	uid = user.uid
	username = user.email
	room = Topic.query.filter_by(topicname=room).first()
	topic_uid = room.uid
	room_name = room.topicname
	message = Message(message['data']['message'], uid, username, topic_uid, room_name)
	db.session.add(message)
	db.session.commit()


@socketio.on('leaveroom', namespace='/chat')
def leaveroom(message):
    room = session.get('room')
    leave_room(room)
    print(session.get('email'))
    print('left room')
    leaveMessage = {'user': session.get('email'), 'msg': session.get('email') + ' has left ' + room + '.'}
    emit('status',leaveMessage, room=room)
    user = User.query.filter_by(email=session.get('email')).first()
    session.pop('room', None)
    user.topic_name = None
    db.session.commit()




if __name__ == '__main__':
	socketio.run(app)
