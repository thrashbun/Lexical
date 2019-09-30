from flask import Flask
app = Flask(__name__)
from Application import views
from flask_socketio import SocketIO
from flask_socketio import send, emit

from Application import model

app.config['SECRET_KEY'] = 'secret!'
socketio = SocketIO(app)


@socketio.on('message')
def handle_message(message):
    send(message)
    
@socketio.on('json')
def handle_json(json):
    print('received json: ' + str(json))
    send(json)
    
@socketio.on('my event')
def handle_message(message):
    print('received message: ' + str(message))
    emit('my response', model.get_table_from_query(message['data']))
    
#socketio.run(app)