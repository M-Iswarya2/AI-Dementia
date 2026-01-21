from django.urls import path
from .views import save_final_score, dashboard_data

urlpatterns = [
    path("save_final_score/", save_final_score, name="save_final_score"),
    path("dashboard-data/", dashboard_data, name="dashboard-data"),  # <-- new
]
