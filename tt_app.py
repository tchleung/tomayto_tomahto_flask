from flask import Flask, flash, render_template, request
from werkzeug.utils import secure_filename
import os
import tensorflow as tf
from helper import wav_to_img
from helper import make_prediction

UPLOAD_FOLDER = './temp_audio/'
ALLOWED_EXTENSIONS = {'wav'}

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
app.config['MAX_CONTENT_LENGTH'] = 512*1024

model = tf.keras.models.load_model('./Model/saved_model.pb)

def allowed_file(filename):
    return '.' in filename and \
        filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

@app.route('/', methods=['POST', 'GET'])
def init_recorder():
    return render_template("index.html")

@app.route('/uploader', methods = ['GET', 'POST'])
def upload_file():
    if request.method == 'POST':
        f = request.files['file']
        if allowed_file(f.filename):
            filename = secure_filename(f.filename)
            f.save(os.path.join(app.config['UPLOAD_FOLDER'],filename))
            test_arr = wav_to_img(os.path.join(app.config['UPLOAD_FOLDER'],filename))
            prediction = make_prediction(model,test_arr)
            os.remove(os.path.join(app.config['UPLOAD_FOLDER'],filename))
            return render_template('prediction.html', message=prediction)
        else:
            return str('Format error, please go back and upload a .wav recording')
if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8080, debug=True)