from flask import Flask
from flask_socketio import SocketIO, send
from dotenv import load_dotenv # to help load env vars from a file.
import os
load_dotenv() # loads the env vars from my .env file

# create the flask app and configure it
app = Flask(__name__)
app.config["SECRET_KEY"] = os.getenv("FLASK_SERVER_SECRET_KEY") # key comes from the env var in the OS

# setup the flask socketio server
socketio_server = SocketIO(app, cors_allowed_origins='*')

# start listening for messages coming thru
@socketio_server.on('message')
def handleMessage(msg):
    print(f'yo message is {msg}')
    send(f'{msg}', broadcast=True)


@app.route("/")
def hello():
  return "What up doe!"

if __name__ == "__main__":
  socketio_server.run(app)