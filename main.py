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

@app.route('/chat/<user>')
def chat(user):
	if 'user' in session:
		return render_template('client.html', user = escape(session['user']))
	else:
		return redirect(url_for('login'))

def messageRecived():
  print( 'message was received!!!' )

@socketio.on( 'message event' )
def handle_my_custom_event( json ):
  print( 'recived my event: ' + str( json ) )
  socketio.emit( 'message_response', json, callback=messageRecived )

if __name__ == '__main__':
	socketio.run(app, debug=True, host='localhost', port=5000)

