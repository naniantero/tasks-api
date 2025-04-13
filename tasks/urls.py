from django.urls import path

from tasks.views import (AssignTaskView, CreateTaskTemplateView, SetTaskCompletedView,
                         SetTaskForReviewView)

app_name = "tasks"

urlpatterns = [
    path('create',
         CreateTaskTemplateView.as_view(), name="create-task"),
    path('<int:task_instance_id>/<int:user_id>/assign',
         AssignTaskView.as_view(), name="assign-task"),
    path('<int:task_instance_id>/<int:user_id>/set-for-review',
         SetTaskForReviewView.as_view(), name="set-for-review"),
        path('<int:task_instance_id>/set-completed',
         SetTaskCompletedView.as_view(), name="set-completed"),
]
