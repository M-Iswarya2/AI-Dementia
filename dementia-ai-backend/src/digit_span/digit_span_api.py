from flask import Blueprint, request, jsonify
from .digit_span_evaluation import evaluate_digit_span

digit_span_bp = Blueprint("digit_span", __name__)

@digit_span_bp.route("/submit", methods=["POST"])
def submit_digit_span():
    """
    Receives digit span results:
    {
        "forward": 5,
        "backward": 4
    }

    Returns:
    {
        success: True,
        forward_score,
        backward_score,
        total_score,
        normalized_score (0–1),
        risk_level
    }
    """

    try:
        data = request.get_json()

        if not data:
            return jsonify({
                "success": False,
                "error": "No data received"
            }), 400

        # Evaluate
        result = evaluate_digit_span(data)

        return jsonify({
            "success": True,
            "forward_score": result["forward_score"],
            "backward_score": result["backward_score"],
            "total_score": result["total_score"],
            "digit_span_score": result["normalized_score"],  # 0–1 scale
            "risk_level": result["risk_level"]
        }), 200

    except Exception as e:
        import traceback
        traceback.print_exc()
        return jsonify({
            "success": False,
            "error": str(e)
        }), 500
