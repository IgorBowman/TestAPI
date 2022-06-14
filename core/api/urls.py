from django.urls import include, path
from rest_framework.routers import DefaultRouter

from api.views import (
    UsersAPIView,
    CurrentUserView,
    CurrentUserPUTCHView,
    PrivateUsersViewSet,
    LoginView,
    LogoutView,
)

router_class = DefaultRouter()
router_class.register('users', PrivateUsersViewSet, basename='private')

urlpatterns = [
    path('user/users/<int:pk>', CurrentUserPUTCHView.as_view(),
         name='current_user_putch'),
    path('user/users/current', CurrentUserView.as_view(),
         name='current_user_information'),
    path('user/users/', UsersAPIView.as_view(),
         name='general_user_information'),
    path('auth/login', LoginView.as_view(), name='login'),
    path('auth/logout', LogoutView.as_view(), name='logout'),
    path('admin/private', include(router_class.urls))
]
