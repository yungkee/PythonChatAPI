from flask import Flask, render_template, session, request
from flask_socketio import SocketIO, emit, join_room, leave_room
from flask import render_template, request, flash, session, url_for, redirect
from validation import RegisterForm, LoginForm, RoomForm
from models import db, User, Topic, Message, BannedUser, Admin
import datetime

app = Flask(__name__)
app.debug = True
app.config['SECRET_KEY'] = '6666'
socketio = SocketIO(app)
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql://root@localhost/development'

db.init_app(app)


def connect(params):
	#Connect to the PostgresSQL database server
	conn = None
	try:
		print("Connecting to the PostgresSQL database....")
		conn = psycopg2.connect(**params)
		return conn
	except(Exception, psycopg2.DatabaseError) as error:
		print(error)
	return conn


@app.route('/')
def home():
	return render_template('home.html')

@app.route('/chat', methods=['GET', 'POST'])
def chat():
	form = RoomForm()
	rooms = Topic.query.all()
	users = User.query.all()
	messages = Message.query.all()
	banned_from = []
	admin_rooms = []

	session['room'] = 'MainChat'

	if 'email' not in session:
		return redirect(url_for('signin'))

	user = User.query.filter_by(email = session['email']).first()

	if BannedUser.query.filter_by(used_id = user.uid).first() is not None:
		flagged_rooms = BannedUser.query.filter_by(user_id = user.uid).all()
		for room in flagged_rooms:
			if room.times_flagged >= 5 and room.topic_id != 1:
				print("banned from:")
				print(room.topic_id)
				banned_from.append(room.topic_id)

	if BannedUser.query.filter_by(user_id=user.uid).first() is not None:
		flagged_rooms = BannedUser.query.filter_by(user_id=user.uid).all()
		for room in flagged_rooms:
			if room.times_flagged >= 5 and room.topic_id != 1:
				print("banned from:")
				print(room.topic_id)
				banned_from.append(room.topic_id)

	if Admin.query.filter_by(user_id=user.uid).first() is not None:
		print("Admin exists")
		admin_for = Admin.query.filter_by(user_id=user.uid).all()
		for room in admin_for:
			print("adm")
			print(room.topic_id)
			if room.topic_id != 1:
				admin_rooms.append(Topic.query.filter_by(uid=room.topic_id).first().topicname)

	if user is None:
		return redirect(url_for('signin'))
	else:
		session['uid'] = user.uid
		if request.method == 'POST':
			if form.validate() == False:
				return render_template('chat.html', form=form, rooms=rooms, users=users, messages=messages, banned_from=banned_from, admin_rooms=admin_rooms)
			else:
				uid = user.uid
				newroom = Topic(form.topicname.data, uid)
				db.session.add(newroom)
				db.session.commit()
				session['topic'] = newroom.topicname
				newroom = Topic.query.filter_by(topicname=form.topicname.data).first()
				mod = Admin(user.uid, newroom.uid)
				db.session.add(mod)
				db.session.commit()
				return redirect('/chat/' + newroom.topicname)
		
		if request.method == 'GET':
			return render_template('chat.html', form=form, topics=topics, users=users, messages=messages, banned_from=banned_from, admin_rooms=admin_rooms)

@app.route('/chat/<chatroom_title>')
def show_chatroom(chatroom_title):
	form = RoomForm()
	rooms = Topic.query.all()
	users = User.query.all()
	messages = Message.query.all()
	banned_from = []
	admin_rooms = []
	banned_user = []

	room = Topic.query.filter_by(topicname = chatroom_title).first()

	user = User.query.filter_by(email = session['email']).first()

	if BannedUser.query.filter_by(user_id = user.uid).first() is not None:
		flagged_rooms = BannedUser.query.filter_by(user_id = user.uid).all()
		for room in flagged_rooms:
			if room.times_flagged >= 5 and room.topic_id != 1:
				print("banned_from:")
				print("room.topic_id")
				banned_from.append(room.topic_id)

	if BannedUser.query.filter_by(user_id = user.uid).first() is not None:
		users = BannedUser.query.filter_by(topic_id = topic.uid).all()
		for local_user in users:
			if local_user in users:
				if local_user.times_flagged >= 5 and room.topic_id != 1:
					print("banned from:")
					print("room.topic_id")
					banned_from.append(room.topic_id)

	if Admin.query.filter_by(user_id = user.uid).first() is not None:
		print("admin exists")
		adm_for = Admin.query.filter_by(user_id = user_uid).all()
		for room in adm_for:
			print("adm")
			print(room.topic_id)
			if room.topic_id != 1:
				admin_rooms.append(Topic.query.filter_by(uid=room.topic_id).first().topicname)

	if room is None:
		return redirect(url_for('chat'))

	if room.uid in banned_from:
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
				return render_template('chat.html', form=form, rooms=rooms, users=users, messages=messages, banned_from = banned_from, admin_rooms = admin_rooms)
			else:
				uid = user.uid
				newroom = Topic(form.topicname.data, uid)
				db.session.add(newroom)
				db.session.commit()
				session['room'] = newroom.topicname
				newroom = Topic.query.filter_by(topicname = form.topicname.data).first()
				adm = Admin(user.uid, newroom.uid)
				db.session.add()
				db.session.commit()
				return redirect('/chat/' + newroom.topicname)
		
		if request.method == 'GET':
			return render_template('chat.html', form=form, rooms=rooms, users=users, messages=messages, banned_from = banned_from, admin_rooms = admin_rooms)


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
			session['username'] = newuser.username
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

@socketio.on('added_admin', namespace='/chat')
def create_room(message):
	print("Added")
	print(message['data']['user'])
	user = User.query.filter_by(email=message['data']['user']).first()
	room = Topic.query.filter_by(topicname=session.get('room')).first()
	adm = Admin(user.uid, room.uid)
	db.session.add(adm)
	db.session.commit()

@socketio.on('removed_admin', namespace='/chat')
def create_room(message):
	print("Removed")
	print(message['data']['user'])
	user = User.query.filter_by(email=message['data']['user']).first()
	room = Topic.query.filter_by(topicname=session.get('room')).first()
	for adm in Admin.query.filter_by(user_id=user.id):
		if adm.topic_id == room.id:
			db.session.delete(mod)
			db.session.commit()

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

@socketio.on('banned', namespace='/chat')
def banned(message):
	print("ban")
	print(message)
	banned_user = User.query.filter_by(username = message['data']['user']).first()
	room = Topic.query.filter_by(topicname = message['data']['room']).first()
	banned_user = BannedUser(banned_user.uid, room.uid)
	banned_user.times_flagged = 500
	banFromRoom(banned_user.user_id, room_uid)
	db.session.add(banned_user)
	db.session.commit()

@socketio.on('unbanned', namespace ='/chat')
def unbanned(message):
	print("unban")
	print(message)
	unbanned_user = User.query.filter_by(username=message['data']['user']).first()
	room = Topic.query.filter_by(topicname=message['data']['room']).first()
	if BannedUser.query.filter_by(user_id = unbanned_user.uid).first() is not None:
		for local_user in BannedUser.query.filter_by(user_id=unbanned_user.uid):
			if local_user.topic_uid == room.uid:
				unbanned_info = {'user': unbanned_user.username,'room': room.topicname}
				emit('unbanned', unbanned_info, broadcast = True)
				db.session.delete(local_user)
				db.session.commit()


def banFromRoom(user_id, room_id):
	user = User.query.filter_by(uid = user_id).first()
	room = Topic.query.filter_by(uid = room_id).first()
	banned_info = {'user': user.username,'room': room.topicname}
	emit('banned', banned_info, broadcast = True)

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

@socketio.on('delete_my_chatroom', namespace='/chat')
def delete_my_chatroom(message):
	print("delete_chatroom")
	print("This is message\n")
	print(message)
	topic_id = message['data']['id']
	parent = message['data']['parent']
	topic = Room.query.filter_by(uid = topic_id).first()
	print("hi")
	for room in BannedUser.query.filter_by(topic_id = topic_id):
		print(room.topic_id)
		db.session.delete(room)
	print("do")
	for adm in Admin.query.filter_by(topic_id = topic_id):
		print(adm.topic_id)
		db.session.delete(adm)
	for message in Message.query.filter_by(topic_name = topic.topicname):
		print(message.text)
		db.session.delete(topic)
	db.session.delete(topic)
	db.session.commit()
	delete_msg = {'msg': parent}
	emit('delete_my_chatroom', delete_msg, broadcast = True)

if __name__ == '__main__':
	socketio.run(app)



