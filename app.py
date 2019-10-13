import handler
import os
import io
import re

from base64 import standard_b64decode
from flask import Flask, url_for, request, redirect
from werkzeug.utils import secure_filename

UPLOAD_FOLDER = './'

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

@app.route('/')
def hello_world():
    return 'welcome to <strong>seamless.</strong>'

@app.route('/scan', methods=['POST'])
def scan():
    data = request.json
    print(data)
    image = io.BytesIO(standard_b64decode(data["data"])) #re.sub("data:image/jpeg;base64", '', data["data"])))
    ret = handler.get_data(image)
    return ret
