from flask import Flask
app = Flask(__name__)
from Application import views
from flask_socketio import SocketIO

app.config['SECRET_KEY'] = 'secret!'
socketio = SocketIO(app)
socketio.run(app)

@socketio.on('message')
def handle_message(message):
    send(message)