import os
import numpy as np
import librosa
from scipy.io import wavfile
from scipy.signal import resample
from tensorflow.keras.models import load_model

# ================= CONFIG =================
SR = 16000       # target sample rate
N_MFCC = 40      # number of MFCC coefficients
MAX_LEN = 300    # number of time frames
MODEL_PATH = "models/dementia_cnn_bilstm.h5"

# ================= LOAD MODEL =================
model = load_model(MODEL_PATH)

# ================= AUDIO FIXING =================
def fix_audio(path, target_rate=SR):
    """
    Reads WAV, converts to mono, resamples to target_rate, and normalizes to [-1,1]
    """
    rate, data = wavfile.read(path)

    # Convert to mono
    if len(data.shape) > 1:
        data = data.mean(axis=1)

    # Normalize to float32 [-1,1]
    if data.dtype == np.int16:
        data = data.astype(np.float32) / 32768.0
    elif data.dtype == np.int32:
        data = data.astype(np.float32) / 2147483648.0
    else:
        data = data.astype(np.float32)

    # Resample if needed
    if rate != target_rate:
        num_samples = int(len(data) * target_rate / rate)
        data = resample(data, num_samples)

    return data, target_rate

# ================= FEATURE EXTRACTION =================
def extract_mfcc_from_data(y, sr=SR):
    """
    Extract MFCCs from a numpy array instead of file
    """
    mfcc = librosa.feature.mfcc(
        y=y,
        sr=sr,
        n_mfcc=N_MFCC
    ).T

    # Pad or truncate
    if mfcc.shape[0] < MAX_LEN:
        pad_width = MAX_LEN - mfcc.shape[0]
        mfcc = np.pad(mfcc, ((0, pad_width), (0, 0)))
    else:
        mfcc = mfcc[:MAX_LEN, :]

    return mfcc

# ================= PREDICTION =================
def predict_voice(file_path):
    y, sr = fix_audio(file_path)
    mfcc = extract_mfcc_from_data(y, sr)
    X = mfcc[np.newaxis, ..., np.newaxis]

    prob_no_dementia = model.predict(X, verbose=0)[0][0]
    label = "no_dementia" if prob_no_dementia >= 0.5 else "dementia"

    return label, float(prob_no_dementia)

# ================= TERMINAL TEST =================
if __name__ == "__main__":
    test_file = "uploads/test_audio.wav"  # replace with your file
    label, prob = predict_voice(test_file)

    print("\n====== VOICE MODEL TEST ======")
    print(f"Prediction            : {label}")
    print(f"No-dementia probability: {prob:.3f}")
    print(f"Dementia risk         : {1 - prob:.3f}")
