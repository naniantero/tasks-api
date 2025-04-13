from django.urls import path
from rest_framework_simplejwt.views import TokenRefreshView

from users.views import (AdminJoinGroupView, CustomTokenObtainPairView,
                         GroupDetailView, JoinGroupWithInviteView,
                         RegisterAdminView)

app_name = "users"

urlpatterns = [
    path('group/<uuid:group_id>/join/',
         AdminJoinGroupView.as_view(), name='join-group'),
    path('register/', RegisterAdminView.as_view(
    ), name='register_admin'),
    path("group/<int:pk>/", GroupDetailView().as_view(),
         name="group-detail"),
    path('token/', CustomTokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('group/join', JoinGroupWithInviteView.as_view(), name='join-group'),
]
