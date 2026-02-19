import os
import librosa
import numpy as np
import pandas as pd

# =====================
# CONFIG
# =====================
DATA_DIR = "dataset/augmented"
SR = 16000
N_MFCC = 40
MAX_LEN = 300
OUTPUT_CSV = "mfcc_dataset.csv"

# =====================
# MFCC FUNCTION
# =====================
def extract_mfcc(file_path):
    y, sr = librosa.load(file_path, sr=SR, mono=True)

    mfcc = librosa.feature.mfcc(
        y=y,
        sr=sr,
        n_mfcc=N_MFCC
    ).T   # (time, mfcc)

    # Pad / truncate
    if mfcc.shape[0] < MAX_LEN:
        pad_width = MAX_LEN - mfcc.shape[0]
        mfcc = np.pad(mfcc, ((0, pad_width), (0, 0)))
    else:
        mfcc = mfcc[:MAX_LEN, :]

    return mfcc

# =====================
# DATASET CREATION
# =====================
rows = []

for label in ["dementia", "no_dementia"]:
    folder = os.path.join(DATA_DIR, label)

    for file in os.listdir(folder):
        if file.endswith(".wav"):
            file_path = os.path.join(folder, file)
            try:
                mfcc = extract_mfcc(file_path)

                # flatten MFCC (300 x 40 → 12000)
                mfcc_flat = mfcc.flatten()

                row = {
                    "filename": file,
                    "label": label
                }

                # store mfcc_0 ... mfcc_11999
                for i, value in enumerate(mfcc_flat):
                    row[f"mfcc_{i}"] = value

                rows.append(row)

            except Exception as e:
                print(f"Error processing {file}: {e}")

# =====================
# SAVE TO CSV
# =====================
df = pd.DataFrame(rows)
df.to_csv(OUTPUT_CSV, index=False)

print("MFCC dataset saved successfully!")
print("Shape:", df.shape)
