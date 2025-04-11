from django.urls import path
from tasks.views import CreateTaskView

PATHS = {
    'create_task': 'create/',
}
app_name = "users"

urlpatterns = [
    path(PATHS['create_task'],
         CreateTaskView.as_view(), name="create-task"),
]
