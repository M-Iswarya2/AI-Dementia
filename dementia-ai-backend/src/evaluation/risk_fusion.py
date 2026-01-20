def fuse_scores(memory, attention, voice, questionnaire):
    """
    Fuse Memory and Attention into a single cognitive score.
    All inputs expected in range 0–1 (decimals).
    Output final_risk_score in range 0–1
    """

    # New Weights
    WEIGHTS = {
        "cognitive": 0.40,    # combined memory + attention
        "voice": 0.40,
        "questionnaire": 0.20
    }

    # Compute combined cognitive score (weighted memory + attention)
    cognitive_score = (memory * 0.6 + attention * 0.4)  # example split: memory 60%, attention 40% of cognitive

    # Compute final weighted score
    final_score = (
        cognitive_score * WEIGHTS["cognitive"] +
        voice * WEIGHTS["voice"] +
        questionnaire * WEIGHTS["questionnaire"]
    )

    # Risk interpretation (inverted)
    if final_score >= 0.80:
        risk_level = "Low Risk"
    elif final_score >= 0.60:
        risk_level = "Mild Cognitive Impairment (Early Signs)"
    elif final_score >= 0.40:
        risk_level = "Medium Risk"
    else:
        risk_level = "High Risk – Clinical Evaluation Recommended"

    return {
        "final_risk_score": round(final_score, 3),
        "risk_level": risk_level,
        "weights_used": WEIGHTS,
        "breakdown": {
            "cognitive": round(cognitive_score * 100, 1),
            "voice": round(voice * 100, 1),
            "questionnaire": round(questionnaire * 100, 1)
        }
    }
