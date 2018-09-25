from source import create_app, socketio
from flask import Flask, render_template, request, redirect, redirect, url_for, session, escape, flash
from flask_socketio import SocketIO, emit

app = create_app()

@app.route('/')
def mainpage(): 
	if 'user' in session:
		flash('You are successfully logged in!')
		return render_template('index.html', login='True')
	else:
		flash('You need register account or login in if you want to use chat')
		return render_template('index.html', login='False')

@app.route('/register', methods=['GET', 'POST']) #regestration
def register():
    if request.method == 'GET':
        return render_template('register.html')
    else:
        return 'error'

@app.route('/login', methods=['GET', 'POST']) #authorization
def login():
    form = 
    if 'user' in session:
        return redirect(url_for('mainpage'))
    else:
        if request.method == 'GET':
            return render_template('login.html')

        elif request.method == 'POST':
            username = request.form['username']
            password = request.form['password']
            session['user'] = username
            return redirect(url_for('chat', user=escape(session['user'])))

@app.route('/logout', methods =['POST'])
def logout():
	session.pop('user', None)
	return redirect(url_for('mainpage'))

@app.route('/chat', methods = ['GET','POST'])
def chat():
    form = MainForm()
    topics = Topic.query.all()

    if 'email' not in session:
        return redirect(url_for('login'))

    user = User.query.filter_by(email = session['email']).first()

    if user is None:
        return redirect(url_for('login'))
    else:
        if reguest.method == 'POST':
            if form.validate() == False:
                return render_template('client.html', form = form, topics = topics)
            else:
                uid = user.uid 
                newtopic = Topic(form.topicname.data, uid)
                db.session.add(newtopic)
                db.session.commit()
                session['topic'] = newtopic.topicname
                return redirec(url_for('chat'))

        if request.method == 'GET':
            return render_template('client.html', form = form, topics = topics)


@socketio.on('message', namespace='/chat')
def chat_message(message):
    print("message = ", message)
    print(message['data']['message'])
    email = session.get('email')
    room = session.get('room')
    emit('message',{'msg': session.get('email') + ':' + message['data']['message']}, room = room)
    user = User.query.filter_by(email = email).first()
    message = Message(message['data']['message'], uid. room.uid)
    db.session.add(message)
    db.session.commit()

if __name__ == '__main__':
	socketio.run(app, debug=True, host='localhost', port=5000)

