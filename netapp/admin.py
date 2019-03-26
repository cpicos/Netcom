from django.contrib import admin

from .models import Client, UserType, EventType, EventSubtype, Event
# Register your models here.

admin.site.register(Client)
admin.site.register(UserType)
admin.site.register(EventType)
admin.site.register(EventSubtype)
admin.site.register(Event)