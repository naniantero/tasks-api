from django.urls import path
from tasks.views import CreateTaskTemplateView


app_name = "tasks"

urlpatterns = [
    path('create',
         CreateTaskTemplateView.as_view(), name="create-task"),
]
