from django.db import models
from django.contrib.auth.models import User

class DementiaAssessment(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    final_score = models.FloatField()
    risk_level = models.CharField(max_length=50)
    created_at = models.DateTimeField(auto_now_add=True)  # must exist

    def __str__(self):
        return f"{self.user.username} - {self.final_score}"
