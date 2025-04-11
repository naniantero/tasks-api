from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),

    # App URLs
    path('users/', include(('users.urls', 'users'), namespace='users')),
    path('tasks/', include('tasks.urls', namespace='tasks')),
    path('rewards/', include('rewards.urls', namespace='rewards')),
]