from flask import Flask, flash, render_template, request
from werkzeug.utils import secure_filename
import os
from helper import load_model
from helper import wav_to_img
from helper import make_prediction

UPLOAD_FOLDER = '/temp_audio/'
ALLOWED_EXTENSIONS = {'wav'}

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
app.config['MAX_CONTENT_LENGTH'] = 512*1024

model = load_model()

def allowed_file(filename):
    return '.' in filename and \
        filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

@app.route('/', methods=['POST', 'GET'])
def init_recorder():
    return render_template("index.html")

@app.route('/predict', methods = ['GET', 'POST'])
def upload_file():
    if request.method == 'POST':
        f = request.files['file']
        if allowed_file(f.filename):
            test_arr = wav_to_img(f)
            prediction = make_prediction(model,test_arr)
            '''
            Old approach saves the uploaded audio in a temp folder, removes it after prediction is made
            Current method just loads it into memory 
            filename = secure_filename(f.filename)
            f.save(os.path.join(app.config['UPLOAD_FOLDER'],filename))
            test_arr = wav_to_img(os.path.join(app.config['UPLOAD_FOLDER'],filename))
            os.remove(os.path.join(app.config['UPLOAD_FOLDER'],filename))
            '''
            return render_template('prediction.html', message=prediction)
        else:
            return str('Format error, please go back and upload a .wav recording')
if __name__ == '__main__':
    # Self-sign SSL to get HTTPS to work, the recorder JS requires HTTPS to work
    # app.run(host='0.0.0.0', port=8080, debug=True, ssl_context='adhoc')
    app.run(host='0.0.0.0', port=8080, debug=True)