def evaluate_digit_span(data):
    """
    Expected data format:
    {
        "forward": 5,
        "backward": 4
    }
    """

    forward = int(data.get("forward", 0))
    backward = int(data.get("backward", 0))

    total_score = forward + backward

    # Normalize to 0–1 scale (max possible = 7 + 6 = 13)
    normalized_score = total_score / 13

    # Risk classification
    if total_score >= 10:
        risk = "Low"
    elif total_score >= 7:
        risk = "Moderate"
    else:
        risk = "High"

    return {
        "forward_score": forward,
        "backward_score": backward,
        "total_score": total_score,
        "normalized_score": round(normalized_score, 3),
        "risk_level": risk
    }
