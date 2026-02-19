import json
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from .trail_logic import evaluate_trail_b


@csrf_exempt
def trail_b_api(request):
    if request.method == "POST":
        data = json.loads(request.body)

        time_taken = data.get("time_taken")
        mistakes = data.get("mistakes")

        result = evaluate_trail_b(time_taken, mistakes)

        return JsonResponse(result)

    return JsonResponse({"error": "Invalid request"}, status=400)
