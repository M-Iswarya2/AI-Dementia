from django.http import JsonResponse
from django.utils import timezone
from .models import DementiaAssessment

def dashboard_data(request):
    user = request.user

    # ----------------- Handle anonymous users -----------------
    if not user.is_authenticated:
        return JsonResponse({
            "current_risk": None,
            "risk_score": None,
            "last_assessment_type": None,
            "last_assessment_date": None,
            "total_assessments": 0,
            "completed_this_month": 0,
            "trend": None,
            "trend_change": None,
            "assessment_history": [],
            "error": "User not logged in"
        }, status=200)  # return 200 so frontend can still render

    # ----------------- Fetch assessments -----------------
    assessments = DementiaAssessment.objects.filter(user=user).order_by('-created_at')

    # If no assessments, return defaults
    if not assessments.exists():
        return JsonResponse({
            "current_risk": None,
            "risk_score": None,
            "last_assessment_type": None,
            "last_assessment_date": None,
            "total_assessments": 0,
            "completed_this_month": 0,
            "trend": None,
            "trend_change": None,
            "assessment_history": []
        })

    latest = assessments.first()

    # ----------------- Build assessment history -----------------
    history = []
    for a in assessments:
        history.append({
            "date": a.created_at.strftime("%Y-%m-%d") if a.created_at else "--",
            "type": "Assessment",
            "risk": a.risk_level or "N/A",
            "score": a.final_score if a.final_score is not None else "--"
        })

    # ----------------- Calculate total this month -----------------
    current_month = timezone.now().month
    completed_this_month = assessments.filter(created_at__month=current_month).count()

    return JsonResponse({
        "current_risk": latest.risk_level or "Not Assessed",
        "risk_score": latest.final_score if latest.final_score is not None else "--",
        "last_assessment_type": "Assessment",
        "last_assessment_date": latest.created_at.strftime("%Y-%m-%d") if latest.created_at else "--",
        "total_assessments": assessments.count(),
        "completed_this_month": completed_this_month,
        "trend": None,           # optional, can calculate if needed
        "trend_change": None,    # optional
        "assessment_history": history
    })
from django.views.decorators.csrf import csrf_exempt
import json

@csrf_exempt
def save_final_score(request):
    if request.method == "POST":
        try:
            data = json.loads(request.body)
            user_id = data.get("user_id")
            final_score = data.get("final_score")
            risk_level = data.get("risk_level")
            assessment_type = data.get("assessment_type", "Flask Evaluation")

            # Save to DB
            assessment = DementiaAssessment.objects.create(
                user_id=user_id,
                final_score=final_score,
                risk_level=risk_level,
                
            )

            return JsonResponse({"success": True, "id": assessment.id})

        except Exception as e:
            return JsonResponse({"success": False, "error": str(e)})

    return JsonResponse({"success": False, "error": "Invalid request method"})
