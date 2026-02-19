import numpy as np
import librosa
from tensorflow.keras.models import load_model


SR = 16000       # expected sample rate
N_MFCC = 40
MAX_LEN = 300
MODEL_PATH = "models/dementia_cnn_bilstm.h5"

model = load_model(MODEL_PATH)

def extract_mfcc(file_path):
    
    y, sr = librosa.load(file_path, sr=SR, mono=True)

    mfcc = librosa.feature.mfcc(
        y=y,
        sr=sr,
        n_mfcc=N_MFCC
    ).T

    # Pad or truncate
    if mfcc.shape[0] < MAX_LEN:
        mfcc = np.pad(
            mfcc,
            ((0, MAX_LEN - mfcc.shape[0]), (0, 0)),
            mode="constant"
        )
    else:
        mfcc = mfcc[:MAX_LEN, :]

    return mfcc


def predict_voice(file_path):
    mfcc = extract_mfcc(file_path)
    X = mfcc[np.newaxis, ..., np.newaxis]

    prob_no_dementia = model.predict(X, verbose=0)[0][0]
    label = "no_dementia" if prob_no_dementia >= 0.5 else "dementia"

    return label, float(prob_no_dementia)


if __name__ == "__main__":
    test_file = "uploads/test_audio.wav"

    label, prob = predict_voice(test_file)

    print("\n====== VOICE MODEL TEST ======")
    print(f"Prediction             : {label}")
    print(f"No-dementia probability: {prob:.3f}")
    print(f"Dementia risk          : {1 - prob:.3f}")
