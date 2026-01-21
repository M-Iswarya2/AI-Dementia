# src/evaluation/final_result.py

from flask import Blueprint, request, jsonify
import requests  # to send data to Django
from .risk_fusion import fuse_scores

evaluation_bp = Blueprint("evaluation", __name__)

DJANGO_API_URL = "http://127.0.0.1:8000/assessments/save_final_score/"  # Django endpoint

@evaluation_bp.route("/final", methods=["POST"])
def final_evaluation():
    try:
        data = request.get_json()
        print("Raw data received:", data)

        # Extract individual scores
        memory = float(data.get("memory_score", 0))
        attention = float(data.get("attention_score", 0))
        voice = float(data.get("voice_score", 0))
        questionnaire = float(data.get("questionnaire_score", 0))

        print(
            f"Scores -> Memory={memory}, Attention={attention}, "
            f"Voice={voice}, Questionnaire={questionnaire}"
        )

        # Fuse scores to get final risk
        result = fuse_scores(memory, attention, voice, questionnaire)

        # Prepare final data
        final_score = result["final_risk_score"]
        risk_level = result["risk_level"]
        user_id = data.get("user_id")  # make sure frontend sends logged-in user ID

        # Optional: send final result to Django
        if user_id:
            try:
                django_payload = {
                    "user_id": user_id,
                    "final_score": final_score,
                    "risk_level": risk_level
                }
                django_response = requests.post(
                    DJANGO_API_URL,
                    json=django_payload,
                    timeout=5
                )
                print("Django response:", django_response.status_code, django_response.text)
            except Exception as dj_err:
                print("Failed to send final score to Django:", dj_err)

        # Return JSON to frontend
        return jsonify({
            "success": True,
            "final_risk_score": final_score,
            "risk_level": risk_level,
            "breakdown": result.get("breakdown", {}),
            "weights_used": result.get("weights_used", {})
        }), 200

    except Exception as e:
        import traceback
        traceback.print_exc()
        return jsonify({
            "success": False,
            "error": str(e)
        }), 500
