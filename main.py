from chatapp import create_app, socketio

app = create_app()

print("Python server running on http://127.0.0.1:5000")
if __name__ == '__main__':
	socketio.run(app, debug=True, host='localhost', port=5000)

