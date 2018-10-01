from flask import Flask, render_template, session, request
from flask_socketio import SocketIO, emit, join_room, leave_room
from flask import render_template, request, flash, session, url_for, redirect
from validation import RegisterForm, LoginForm, RoomForm
from models import db, User, Room, Message

app = Flask(__name__)
app.debug = True
app.config['SECRET_KEY'] = '6666'
socketio = SocketIO(app)
app.config['SQLALCHEMY_DATABASE_URI'] = ''

db.init_app(app)


def connectToDB():
	connectionString = ''
	try:
		return psycopg2.connect(connectionString)
	except:
		print('Cant` connect to database')



@app.route('/')
def home():
	return render_template('home.html')

@app.route('/chat', methods=['GET', 'POST'])
def chat():
	form = RoomForm()
	users = User.query.all()

	if 'email' not in session:
		return redirect(url_for('login'))

	user = User.query.filter_by(email = session['email']).first()

	if user is None:
		return redirect(url_for('login'))
	else:
		if request.method == 'POST':
			if form.validate() == False:
				return render_template('chat.html', form=form, users=users)
			else:
				uid = user.uid
				newroom = Room(form.roomname.data, uid)
				session['room'] = newroom.roomname
				return redirect(url_for('chat'))
		
		if request.method == 'GET':
			return render_template('chat.html', form=form, users=users)

@app.route('/register', methods=['GET', 'POST'])
def register():
	form = RegisterForm()

	session['room'] = ''

	if 'email' in session:
		return redirect(url_for('chat')) 
	
	if request.method == 'POST':
		if form.validate() == False:
			return render_template('register.html', form=form)
		else:
			newuser = User(form.username, form.email.data, form.password.data)
			db.session.add(newuser)
			db.session.commit()
			session['email'] = newuser.email
			return redirect(url_for('chat'))
	
	if request.method == 'GET':
		return render_template('register.html', form=form)

@app.route('/login', methods=['GET', 'POST'])
def login():
	form = LoginForm()

	session['room'] = 'main chat'

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

@app.route('/logout')
def logout():
	if 'email' not in session:
		return redirect(url_for('login'))

	session.pop('email', None)
	session.pop('room', None)
	return redirect(url_for('login'))

@socketio.on('joinroom', namespace='/chat')
def joinroom(message):
	print('message =', message)
	room = message['data']['room']
	session['room'] = room
	join_room(room)
	print(session.get('email'))
	print('has joined')
	joinMessage = {'msg': session.get('email') + 'has joined ' + room + '.'}
	emit('status', joinMessage, broadcast = True, room=room)


@socketio.on('leaveroom', namespace='/chat')
def leaveroom(message):
    room = session.get('room')
    leave_room(room)
    print(session.get('username'))
    print('left room')
    leaveMessage = {'msg': session.get('username') + 'has left' + room + '.'}
    emit('status', leaveMessage, room=room)
    session.pop('room', None)

@socketio.on('createroom', namespace='/chat')
def createroom(message):
	print("New room\n")
	print(message)
	print(message['data']['room'])
	emit('update_topics', {'msg': { 'room': message['data']['room'] }}, broadcast=True)

print("Python server running on http://127.0.0.1:5000")
if __name__ == '__main__':
	socketio.run(app)


