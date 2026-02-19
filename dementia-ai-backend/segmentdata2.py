import os
import librosa
import numpy as np
import soundfile as sf
import random

# ================= CONFIG =================
BASE_DIR = "dataset"
INPUT_AUDIO_DIR = os.path.join(BASE_DIR, "audio")
OUTPUT_AUG_DIR = os.path.join(BASE_DIR, "augmented")

SR = 16000
DEMENTIA_SEG_SEC = 15
NO_DEMENTIA_SEG_SEC = 30
AUG_PER_SEG = 2

os.makedirs(os.path.join(OUTPUT_AUG_DIR, "dementia"), exist_ok=True)
os.makedirs(os.path.join(OUTPUT_AUG_DIR, "no_dementia"), exist_ok=True)


def augment_dementia(y, sr):
    aug = y.copy()


    n_steps = random.uniform(-1.5, 1.5)
    aug = librosa.effects.pitch_shift(aug, sr=sr, n_steps=n_steps)


    rate = random.uniform(0.9, 1.1)
    aug = librosa.effects.time_stretch(aug, rate=rate)


    aug += np.random.randn(len(aug)) * 0.003
    return aug


def augment_no_dementia(y):
    aug = y.copy()

 
    aug += np.random.randn(len(aug)) * 0.001


    gain = random.uniform(0.95, 1.05)
    aug *= gain
    return aug


def segment_audio(y, sr, segment_sec):
    seg_len = segment_sec * sr
    return [
        y[i:i + seg_len]
        for i in range(0, len(y) - seg_len + 1, seg_len)
    ]

print("Processing dementia...")

for file in os.listdir(os.path.join(INPUT_AUDIO_DIR, "dementia")):
    if not file.lower().endswith(".wav"):
        continue

    y, sr = librosa.load(
        os.path.join(INPUT_AUDIO_DIR, "dementia", file),
        sr=SR
    )

    for i, seg in enumerate(segment_audio(y, sr, DEMENTIA_SEG_SEC)):
        base = file.replace(".wav", f"_seg{i}")

        sf.write(
            os.path.join(OUTPUT_AUG_DIR, "dementia", base + "_orig.wav"),
            seg, sr
        )

        for a in range(AUG_PER_SEG):
            sf.write(
                os.path.join(
                    OUTPUT_AUG_DIR,
                    "dementia",
                    base + f"_aug{a+1}.wav"
                ),
                augment_dementia(seg, sr),
                sr
            )

print("Processing no_dementia...")

for file in os.listdir(os.path.join(INPUT_AUDIO_DIR, "no_dementia")):
    if not file.lower().endswith(".wav"):
        continue

    y, sr = librosa.load(
        os.path.join(INPUT_AUDIO_DIR, "no_dementia", file),
        sr=SR
    )

    for i, seg in enumerate(segment_audio(y, sr, NO_DEMENTIA_SEG_SEC)):
        base = file.replace(".wav", f"_seg{i}")

        sf.write(
            os.path.join(OUTPUT_AUG_DIR, "no_dementia", base + "_orig.wav"),
            seg, sr
        )

        for a in range(AUG_PER_SEG):
            sf.write(
                os.path.join(
                    OUTPUT_AUG_DIR,
                    "no_dementia",
                    base + f"_aug{a+1}.wav"
                ),
                augment_no_dementia(seg),
                sr
            )

print(" All segmentation & augmentation completed successfully.")
