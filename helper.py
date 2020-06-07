import tensorflow as tf
import librosa
import numpy as np

def load_model():
    model = tf.keras.models.load_model('Model')
    return model

def wav_to_img(path):
    audio, sr = librosa.load(path,duration=2.97)
    # parameters for calculating spectrogram in mel scale
    fmax = 10000 # maximum frequency considered
    fft_window_points = 512
    # fft_window_dur = fft_window_points * 1.0 / sr
    hop_size = int(fft_window_points/ 2) # 50% overlap between consecutive frames
    n_mels = 128
    spec = librosa.feature.melspectrogram(audio, sr=sr, n_mels=n_mels, n_fft=fft_window_points, hop_length=hop_size, fmax=fmax)
    spec_gram = librosa.power_to_db(spec, np.max)
    try:
        return librosa.util.pad_center(spec_gram, size = 256, axis = 1)
    except:
        return spec_gram

def make_prediction(model, arr):
    labels = ['Mainland China','Taiwan']
    arr = arr.reshape(1,128,256,1)
    prediction = model.predict(arr)
    pred_label = np.argmax(prediction)
    origin = labels[pred_label]
    return origin