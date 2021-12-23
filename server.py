from flask import Flask, request
from flask_socketio import SocketIO, emit, send, join_room
from dotenv import load_dotenv # to help load env vars from a file.
import os
load_dotenv() # loads the env vars from my .env file

# different apps that can be connected to via rooms
APPS = [
    'SMBN'
]
# address of the raspberry pi brain backend
BRAIN_ADDR = None

# create the flask app and configure it
app = Flask(__name__)
app.config["SECRET_KEY"] = os.getenv("FLASK_SERVER_SECRET_KEY") # key comes from the env var in the OS

# setup the flask socketio server
socketio_server = SocketIO(app, cors_allowed_origins='*')

# frontend apps will emit this event when they connect, therefore this is the handler
@socketio_server.on('frontend interface joining server')
def frontend_joining(data):
    # get the ip address of the connecting app
    ip_addr = request.environ['REMOTE_ADDR']
    
    # establish p2p connection with backend brain
   
    # break the frontend's connection to this socket server

    
# the raspberry pi will emit this event when it connects, this is the handler
@socketio_server.on('backend brain joining server')
def brain_joining(args):
    # get the ip address of the raspberry pi brain and save it
    BRAIN_ADDR = request.environ['REMOTE_ADDR']

@app.route("/")
def hello():
  return "What up doe!"

if __name__ == "__main__":
  socketio_server.run(app)