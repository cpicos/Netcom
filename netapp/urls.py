from django.urls import path

from rest_framework.routers import DefaultRouter

from .views import HomeTemplate

from .apiviews import LoginView, LogoutView


urlpatterns = [
    path("", LoginView.as_view(), name="login"),
    path("logout/", LogoutView.as_view(), name="logout"),
    path("home/", HomeTemplate.as_view(), name="home"),
    
]
