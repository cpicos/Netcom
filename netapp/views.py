from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
from django.views.generic import TemplateView

# Create your views here.

@method_decorator(login_required, name='dispatch')
class HomeTemplate(TemplateView):
    template_name = "home.html"


@method_decorator(login_required, name='dispatch')
class UsersTemplate(TemplateView):
    template_name = "users.html"

@method_decorator(login_required, name='dispatch')
class ClientsTemplate(TemplateView):
    template_name = "clients.html"


@method_decorator(login_required, name='dispatch')
class ScheduleTemplate(TemplateView):
    template_name = "schedule.html"


@method_decorator(login_required, name='dispatch')
class MyScheduleTemplate(TemplateView):
    template_name = "myschedule.html"