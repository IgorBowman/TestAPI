from django.contrib import admin
from django.urls import path, include

from api.views import LoginView, ProfileView

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api-auth/', include('rest_framework.urls')),
]
