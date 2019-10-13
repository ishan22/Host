import handler
from flask import Flask
from werkzeug.utils import secure_filename

UPLOAD_FOLDER = './uploads'

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

@app.route('/')
def hello_world():
    return 'hello world'

@app.route('/scan/<path:imgpath>')
def scan(imgpath):
    print('imgpath%s'%imgpath)
    return ''

@app.route('/scan', methods=['POST'])
def scan_image():
    if 'file' not in request.files:
        flash('No file part')
        return 'FILE ERR'
    imgFile = flask.request.files['file']
    filename = secure_filename(imgFile.filename)
    print("Uploaded file:%s"%filename)
    imgFile.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
    imgData = imgFile.getvalue()
    print(imgData)
    details = handler.get_details(imgData)
    return redirect(url_for('upload_file', filename=filename))
