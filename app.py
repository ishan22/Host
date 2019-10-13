import handler
import os
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
    return data['data']


@app.route('/scan2', methods=['POST'])
def scan_image():
    print(request.files)
    if 'file' not in request.files:
        return 'FILE ERR'
    imgFile = request.files['file']
    filename = secure_filename(imgFile.filename)
    print("Uploaded file:%s"%filename)
    imgFile.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
    with open(filename, 'r') as f:
        imgData = f.getvalue()
    #imgData = imgFile.getvalue()
    print(imgData)
    details = handler.get_details(imgData)
    return redirect(url_for('upload_file', filename=filename))
