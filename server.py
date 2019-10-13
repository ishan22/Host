from flask import Flask

app = Flask(__name__)

# BACKEND/HOST

@app.route('/')
def hello_world():
    return 'Hello, World!'

@app.route('/getPid')
def get_pid(auth_token):
    if !auth_token:
        return err (403 authorization err)
    if pid:
        return pid
    return create_pid()

@app.route('/sortQueue')
def sort():
    return 'SORTED'

@app.route('/getQueue')
def getQueue():
    return 'queue'

@app.route('/getNextSong')
def getNextSong():
    return 'song'

def create_pid():
    # create pid
    # return


# USER

@app.route('/search')
def search():
    return 'searched'

def join_party():


