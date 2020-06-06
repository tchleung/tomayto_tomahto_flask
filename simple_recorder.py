from flask import Flask, render_template, request
from werkzeug.utils import secure_filename
import os
from helper import load_model
from helper import wav_to_img
from helper import make_prediction

UPLOAD_FOLDER = '/upload_folder/'
app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

model = load_model()

@app.route('/', methods=['POST', 'GET'])
def init_recorder():
    return render_template("index.html")

@app.route('/uploader', methods = ['GET', 'POST'])
def upload_file():
   if request.method == 'POST':
      f = request.files['file']
      f.save('temp.wav')
      test_arr = wav_to_img('temp.wav')
      prediction = make_prediction(model,test_arr)
      return render_template('prediction.html', message=prediction) 

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8080, debug=True)