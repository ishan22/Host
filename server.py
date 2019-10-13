from flask import Flask

app = Flask(__name__)

# BACKEND/HOST

@app.route('/')
def hello_world():
    return 'Hello, World!'

@app.route('/add')
def add_event():

