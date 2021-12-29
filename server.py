from flask import Flask, request
from flask_socketio import SocketIO, disconnect, emit, send, join_room
from dotenv import load_dotenv # to help load env vars from a file.
import os
load_dotenv() # loads the env vars from my .env file

# different apps that can be connected to via rooms
APPS = [
    'SMBN'
]
# address of the raspberry pi brain backend
brain_info = {
    "addr": None,
    "dport": None,
    "sid": None
}

# create the flask app and configure it
app = Flask(__name__)
app.config["SECRET_KEY"] = os.getenv("FLASK_SERVER_SECRET_KEY") # key comes from the env var in the OS

# setup the flask socketio server
socketio_server = SocketIO(app, cors_allowed_origins='*')

# frontend apps will emit this event when they connect, therefore this is the handler
@socketio_server.on('frontend interface joining server')
def frontend_joining(dport):
    # get the ip address of the connecting app
    ip_addr = request.environ['REMOTE_ADDR']
    # emit new client connected to raspberry pi with the dport and ip_addr of the client
    emit('new client connected', {
        ip_addr: ip_addr,
        dport: dport
    })
    # emit server address to client
    emit('server address', {
        ip_addr: brain_info['addr'],
        dport: brain_info['dport']
    })
    print('\n\nSent the Brain: \nip_addr: {} \ndport: {} '.format(ip_addr, dport))
    print('\n\nSent the Client: \nip_addr: {} \ndport: {} '.format(brain_info['addr'], brain_info['dport']))
    # disconnect the client from the rendezvous server
    disconnect()
    
# the raspberry pi will emit this event when it connects, this is the handler
@socketio_server.on('backend brain joining server')
def brain_joining(dport_num):
    # get the ip address of the raspberry pi brain and save it
    brain_info['addr'] = request.environ['REMOTE_ADDR']
    # also save the destination port the client sends
    brain_info['dport'] = dport_num
    print('\nBrain has joined da server!!! \nIP Address: {}\nDestination Port: {}\n'.format(brain_info['addr'], brain_info['dport']))

@app.route("/")
def hello():
  return "What up doe!!"

if __name__ == "__main__":
    if app.config['ENV'] == 'development':
        socketio_server.run(app)
    else:
        app.run()