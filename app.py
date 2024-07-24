from flask import Flask, render_template
from flask_socketio import SocketIO, emit
import time
import threading

app = Flask(__name__)
socketio = SocketIO(app)

thread = None

def background_thread():
    """Example of a background thread that sends server-generated events to clients."""
    while True:
        time.sleep(1)
        unix_time = int(time.time())
        socketio.emit('server_update', {'data': f'Unix time: {unix_time}'})

@app.route('/')
def index():
    return render_template('index.html')

@socketio.on('connect')
def handle_connect():
    print('Client connected')
    emit('server_update', {'data': 'Socket connected'})

@socketio.on('start_updates')
def start_updates():
    global thread
    if thread is None:
        thread = threading.Thread(target=background_thread)
        thread.start()
    emit('server_update', {'data': 'Started sending updates'})

if __name__ == '__main__':
    socketio.run(app, debug=True)
