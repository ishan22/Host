import handler
import os
import io
import re
import datetime

from base64 import b64decode
from flask import Flask, url_for, request, redirect
from werkzeug.utils import secure_filename

UPLOAD_FOLDER = './'

app = Flask(__name__)

@app.route('/')
def hello_world():
    return 'welcome to <strong>seamless.</strong>'

@app.route('/scan', methods=['POST'])
def scan():
    data = request.json
    print(data)
    image = io.BytesIO(bytes(b64decode(re.sub("data:image/jpeg;base64", '', data["data"]))))
    ret = handler.get_data(image)
    print(ret['standard'])
    date = ret['standard'].date
    time = ret['standard'].time
    conc = "&{}|&{}|&{}".format(ret["title"], date, time)
    return conc
