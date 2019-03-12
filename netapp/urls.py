from django.urls import path

from rest_framework.routers import DefaultRouter

from .views import HomeTemplate, UsersTemplate

from .apiviews import LoginView, LogoutView, UserViewSet

router = DefaultRouter()
router.register('api/users', UserViewSet, base_name='api/users')

urlpatterns = [
    path("", LoginView.as_view(), name="login"),
    path("logout/", LogoutView.as_view(), name="logout"),
    path("home/", HomeTemplate.as_view(), name="home"),
    path("users/", UsersTemplate.as_view(), name="users"),
    
]

urlpatterns += router.urls
