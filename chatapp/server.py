from flask import Flask, request, session, escape, flash, render_template, url_for, flash, redirect
from chatapp import app

@app.route('/')
def index():
    return render_template('index.hmtl')



@app.route('/register', methods=['GET', 'POST']) #regestration
def register():
    if request.method == 'GET':
        return render_template('register.html')
    else:
        return 'error'

@app.route('/login', methods=['GET', 'POST']) #authorization
def login():
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