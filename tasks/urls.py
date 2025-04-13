from django.urls import path

from tasks.views import AssignTaskView, CreateTaskTemplateView

app_name = "tasks"

urlpatterns = [
    path('create',
         CreateTaskTemplateView.as_view(), name="create-task"),
    path('assign/<str:task_id>/<int:user_id>',
         AssignTaskView.as_view(), name="assign-task")
]
