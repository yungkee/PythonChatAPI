from flask import Flask, request, session, escape, flash, render_template, url_for, flash, redirect
from chatapp import app
from validation import RegisterForm, LoginForm, RoomForm
from models import db, User, Room, Message

@app.route('/')
def index():
    return render_template('index.hmtl')


@app.route('/register', methods=['GET', 'POST']) 
def register():
    form = RegisterForm()

    session['room'] = 'General'

    if 'email' in session:
        return redirect(url_for('chat'))

    if request.method == 'POST':
        if form.validate() == False:
            return render_template('register.html', form=form)
        else:
            new_user = User(form.username.data, form.email.data, form.password.data)
            db.session.add(new_user)
            db.session.commit()
            session['email'] = new_user.email
            return redirect(url_for('chat'))

    if request.method == 'GET':
        return render_template('register.html', form = form)

@app.route('/login', methods=['GET', 'POST']) #authorization
def login():
    form = LoginForm()

    session['room'] = 'General'

    if 'email' in session:
        return redirect(url_for('chat'))

    if request.method == 'POST':
        if form.validate() == False:
            return render_template('login.html', form = form)
        else:
            session['email'] = form.email.data
            return redirect(url_for('chat'))

    elif request.method == 'GET':
        return render_template('login.html', form = form)


@app.route('/logout', methods =['POST'])
def logout():
    session.pop('user', None)
    return redirect(url_for('mainpage'))

@app.route('/chat', methods = ['GET','POST'])
def chat():
    form = RoomForm()
    session['room'] = 'General'

    if 'email' not in session:
        return redirect(url_for('login'))

    user = User.query.filter_by(email = session['email']).first()

    if user is None:
        return redirect(url_for('login'))
    else:
        pass

        if request.method == 'GET':
            return render_template('chat.html', form = form, topics = topics)


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