from django.urls import path

from rest_framework.routers import DefaultRouter

from .views import HomeTemplate, UsersTemplate, ClientsTemplate, ScheduleTemplate, MyScheduleTemplate

from .apiviews import LoginView, LogoutView, UserViewSet, ClientViewSet, UserPermViewSet, CompanyHoursViewSet, \
    EventSubtypeViewSet, EventTypeViewSet, EventViewSet, MyEventsViewSet

router = DefaultRouter()
router.register('api/users', UserViewSet, base_name='api/users')
router.register('api/clients', ClientViewSet, base_name='api/clients')
router.register('api/userperms', UserPermViewSet, base_name='api/userperms')
router.register('api/schedule', CompanyHoursViewSet, base_name='api/schedule')
router.register('api/subtypes', EventSubtypeViewSet, base_name='api/subtypes')
router.register('api/eventtype', EventTypeViewSet, base_name='api/eventtype')
router.register('api/events', EventViewSet, base_name='api/events')
router.register('api/myevents', MyEventsViewSet, base_name='api/myevents')

urlpatterns = [
    path("", LoginView.as_view(), name="login"),
    path("logout/", LogoutView.as_view(), name="logout"),
    path("home/", HomeTemplate.as_view(), name="home"),
    path("users/", UsersTemplate.as_view(), name="users"),
    path("clients/", ClientsTemplate.as_view(), name="clients"),
    path("schedule/", ScheduleTemplate.as_view(), name="schedule"),
    path("myschedule/", MyScheduleTemplate.as_view(), name="myschedule"),
    
]

urlpatterns += router.urls
