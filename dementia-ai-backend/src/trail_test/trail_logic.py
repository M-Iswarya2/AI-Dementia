def evaluate_trail_b(time_taken, mistakes):
    """
    Trail Making Test – Part B evaluation
    """

    # Raw score calculation
    score = max(0, 100 - (time_taken * 0.8) - (mistakes * 5))

    # Risk interpretation
    if time_taken <= 60 and mistakes <= 1:
        risk = "Low"
    elif time_taken <= 120 and mistakes <= 3:
        risk = "Moderate"
    else:
        risk = "High"

    return {
        "test": "Trail Making Test - Part B",
        "time_taken": time_taken,
        "mistakes": mistakes,
        "score": round(score, 2),
        "risk": risk
    }
