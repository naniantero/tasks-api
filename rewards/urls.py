from django.urls import path
from rewards.views import CreateRewardView

PATHS = {
    'create_reward': 'create/',
}
app_name = "users"

urlpatterns = [
    path(PATHS['create_reward'],
         CreateRewardView.as_view(), name="create-reward"),
]
