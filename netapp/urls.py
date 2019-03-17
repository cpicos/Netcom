from django.urls import path

from rest_framework.routers import DefaultRouter

from .views import HomeTemplate, UsersTemplate, ClientsTemplate

from .apiviews import LoginView, LogoutView, UserViewSet, ClientViewSet

router = DefaultRouter()
router.register('api/users', UserViewSet, base_name='api/users')
router.register('api/clients', ClientViewSet, base_name='api/clients')

urlpatterns = [
    path("", LoginView.as_view(), name="login"),
    path("logout/", LogoutView.as_view(), name="logout"),
    path("home/", HomeTemplate.as_view(), name="home"),
    path("users/", UsersTemplate.as_view(), name="users"),
    path("clients/", ClientsTemplate.as_view(), name="clients"),
    
]

urlpatterns += router.urls
