# digit_span_logic.py

def evaluate_digit_span(forward_score, backward_score):
    """
    Evaluate digit span performance.
    Returns normalized score between 0 and 1.
    """

    total = forward_score + backward_score
    normalized = total / 10  # max possible 10

    normalized = max(0.0, min(1.0, normalized))

    return {
        "total_score": total,
        "normalized_score": normalized
    }