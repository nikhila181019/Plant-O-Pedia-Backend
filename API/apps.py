from django.apps import AppConfig
from roboflow import Roboflow


class ApiConfig(AppConfig):
    default_auto_field = "django.db.models.BigAutoField"
    name = "API"
    rf = Roboflow(api_key="sYL2l7TDq7rCJfM6DrA1")
    project = rf.workspace().project("ayurved")
    trained_model = project.version(2).model
