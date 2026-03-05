import os
import numpy as np
import librosa
import tensorflow as tf
from sklearn.preprocessing import LabelEncoder
from sklearn.model_selection import train_test_split
from sklearn.metrics import (
    classification_report,
    confusion_matrix,
    accuracy_score,
    precision_score,
    recall_score,
    f1_score,
    roc_auc_score
)

# ---------------- CONFIG ----------------
DATA_DIR = "dataset/augmented"
MODEL_PATH = "models/dementia_cnn_bilstm_gem.h5"

SR = 16000
N_MFCC = 40
MAX_LEN = 300

# ---------------- MFCC EXTRACTION ----------------
def extract_mfcc(file_path):
    y, sr = librosa.load(file_path, sr=SR, mono=True)
    y, _ = librosa.effects.trim(y)

    if len(y) > 0:
        y = librosa.util.normalize(y)

    mfcc = librosa.feature.mfcc(y=y, sr=sr, n_mfcc=N_MFCC)
    mfcc = mfcc.T

    mfcc = (mfcc - np.mean(mfcc)) / (np.std(mfcc) + 1e-8)

    if mfcc.shape[0] < MAX_LEN:
        pad_width = MAX_LEN - mfcc.shape[0]
        mfcc = np.pad(mfcc, ((0, pad_width), (0, 0)), mode='constant')
    else:
        mfcc = mfcc[:MAX_LEN, :]

    return mfcc


# ---------------- LOAD DATA ----------------
print("Loading dataset for evaluation...")

X, y = [], []

for label in ["dementia", "no_dementia"]:
    folder = os.path.join(DATA_DIR, label)
    if not os.path.exists(folder):
        continue

    for file in os.listdir(folder):
        if file.endswith(".wav"):
            feat = extract_mfcc(os.path.join(folder, file))
            X.append(feat)
            y.append(label)

X = np.array(X)
X = X[..., np.newaxis]

le = LabelEncoder()
y = le.fit_transform(y)

# Use same split as training
X_train, X_test, y_train, y_test = train_test_split(
    X, y, test_size=0.2, stratify=y, random_state=42
)

# ---------------- LOAD MODEL ----------------
print("Loading model...")
model = tf.keras.models.load_model(MODEL_PATH)

# ---------------- PREDICTIONS ----------------
y_probs = model.predict(X_test)
y_pred = (y_probs > 0.5).astype(int)

# ---------------- METRICS ----------------
accuracy = accuracy_score(y_test, y_pred)
precision = precision_score(y_test, y_pred)
recall = recall_score(y_test, y_pred)
f1 = f1_score(y_test, y_pred)
roc_auc = roc_auc_score(y_test, y_probs)

print("\n===== MODEL EVALUATION =====")
print(f"Accuracy  : {accuracy:.4f}")
print(f"Precision : {precision:.4f}")
print(f"Recall    : {recall:.4f}")
print(f"F1 Score  : {f1:.4f}")
print(f"ROC-AUC   : {roc_auc:.4f}")

print("\nConfusion Matrix:")
print(confusion_matrix(y_test, y_pred))

print("\nClassification Report:")
print(classification_report(y_test, y_pred, target_names=le.classes_))