from django.urls import path
from users.views import CreateGroupView, GroupDetailView, JoinGroupView

app_name = "users"

urlpatterns = [
    path('group/<uuid:group_id>/join/',
         JoinGroupView.as_view(), name='join-group'),

    path('group', CreateGroupView.as_view(
    ), name='group'),
    path("group/<int:pk>/", GroupDetailView().as_view(),
         name="group-detail"),  # for get/update/delete
]
