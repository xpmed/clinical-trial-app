from django.contrib import admin
from django.urls import path, include

from .views import DashboardView


urlpatterns = [
    path('admin/', admin.site.urls),

    path('', DashboardView.as_view(), name='dashboard'),

    # Users
    path("users/", include("users.urls")),
]
