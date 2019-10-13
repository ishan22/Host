import firebase_admin
from firebase_admin import credentials
from firebase_admin import db
from flask import Flask

import requests

host_url = 'https://hostdb-153c4.firebaseio.com/'
cred = credentials.Certificate("./serviceAccountKey.json")
firebase_admin.initialize_app(cred, {'databaseURL':host_url})

db_root = db.reference('/')

app = Flask(__name__)


# BACKEND/HOST

@app.route('/')
def hello_world():
    return addPartyToDB('abcd')

def addPartyToDB(pid):
    parties_ref = db_root.child('parties')
    parties_ref.child(pid).set({'pid':pid, 'queue':['me no evil']})
    return 'updated'

@app.route('/getPid')
def get_pid(auth_token):
    #if !auth_token:
     #   return err (403 authorization err)
    #if pid:
    #    return pid
    #return create_pid()
    return 'pid'

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
    return 'created'
    # create pid
    # return


# USER

@app.route('/search')
def search():
    return 'searched'

def join_party():
    return false

