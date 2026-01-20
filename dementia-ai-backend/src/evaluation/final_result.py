from flask import Blueprint, request, jsonify
from .risk_fusion import fuse_scores

evaluation_bp = Blueprint("evaluation", __name__)

@evaluation_bp.route("/final", methods=["POST"])
def final_evaluation():
    try:
        data = request.get_json()
        print("Raw data received:", data)

        memory = float(data.get("memory_score", 0))
        attention = float(data.get("attention_score", 0))
        voice = float(data.get("voice_score", 0))
        questionnaire = float(data.get("questionnaire_score", 0))

        print(
            f"Scores -> Memory={memory}, Attention={attention}, "
            f"Voice={voice}, Questionnaire={questionnaire}"
        )

        result = fuse_scores(memory, attention, voice, questionnaire)

        return jsonify({
            "success": True,

            # Main outputs (as percentage for display)
            "final_risk_score": result["final_risk_score"],
            "risk_level": result["risk_level"],

            # Individual test scores (as percentages)
            "breakdown": result["breakdown"],
            
            # Weights used
            "weights_used": result["weights_used"]
        }), 200

    except Exception as e:
        import traceback
        traceback.print_exc()
        return jsonify({
            "success": False,
            "error": str(e)
        }), 500