from django.contrib import admin

from .models import Client, UserType
# Register your models here.

admin.site.register(Client)
admin.site.register(UserType)