import librosa

y, sr = librosa.load(r"C:\Dementia_ml\dementia-ai-backend\uploads\test_audio.wav", sr=22050)
print(len(y), sr)
