from flask import Flask

app = Flask(__name__)

@app.route('/')
def hello_world():
    return 'Hello, World!'


@app.route('/getPid')
def get_pid():
    return 'PID'


@app.route('/sortQueue')
def sort():
    return 'SORTED'

@app.route('/getQueue')
def getQueue():
    return 'queue'

@app.route('/search')
def search():
    return 'searched'

@app.route('/getNextSong')
def getNextSong():
    return 'song'
