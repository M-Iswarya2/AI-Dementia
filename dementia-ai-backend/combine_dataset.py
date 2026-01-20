import pandas as pd
import numpy as np
import os

# ----------------- Setup -----------------
os.makedirs("dataset", exist_ok=True)
np.random.seed(42)
n_samples = 100

# ----------------- Generate health scores (0 = bad, 1 = good) -----------------
memory_score = np.round(np.random.rand(n_samples), 2)
voice_score = np.round(np.random.rand(n_samples), 2)
questionnaire_score = np.round(np.random.rand(n_samples), 2)

# ----------------- Convert to risk scores (1 = high risk) -----------------
mem_risk = 1 - memory_score
voice_risk = 1 - voice_score
ques_risk = 1 - questionnaire_score

# ----------------- Weighted risk fusion -----------------
weights = {
    "memory": 0.4,
    "voice": 0.35,
    "questionnaire": 0.25
}

final_risk_score = (
    mem_risk * weights["memory"] +
    voice_risk * weights["voice"] +
    ques_risk * weights["questionnaire"]
)

# ----------------- Assign risk labels -----------------
risk_label = []
for i, frs in enumerate(final_risk_score):

    # SAFETY OVERRIDE:
    # If any single modality is extremely poor → High risk
    if memory_score[i] < 0.15 or voice_score[i] < 0.15:
        risk_label.append("High")

    elif frs < 0.35:
        risk_label.append("Low")

    elif frs < 0.6:
        risk_label.append("Medium")

    else:
        risk_label.append("High")

# ----------------- Create dataset -----------------
df = pd.DataFrame({
    "memory_score": memory_score,
    "voice_score": voice_score,
    "questionnaire_score": questionnaire_score,
    "risk_label": risk_label
})

df.to_csv("dataset/fusion_dataset.csv", index=False)
print("fusion_dataset.csv created with clinically consistent labels.")
