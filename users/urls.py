from django.urls import path
from rest_framework_simplejwt.views import TokenRefreshView

from users.views import (AdminJoinGroupView, CustomTokenObtainPairView,
                         GroupDetailView, AcceptInviteView,
                         GetInviteUrlView, AdminRegisterView)

app_name = "users"

urlpatterns = [
    path('group/accept-invite', AcceptInviteView.as_view(),
         name='accept-invite'),
    path('invite-url', GetInviteUrlView.as_view(), name='invite-url'),
    path('group/<uuid:group_id>/admin-join/',
         AdminJoinGroupView.as_view(), name='admin-join-group'),
    path('register/', AdminRegisterView.as_view(
    ), name='register_admin'),
    path("group/<int:pk>/", GroupDetailView().as_view(),
         name="group-detail"),
    path('token/', CustomTokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
]
