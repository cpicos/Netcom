from django.contrib.auth.models import User
from django.db import models

# Create your models here.
class Client(models.Model):
    name = models.CharField(max_length=250)
    dba = models.CharField(max_length=250)
    rfc = models.CharField(max_length=20)
    address = models.CharField(max_length=250)
    postal_code = models.CharField(max_length=20)
    created_at = models.DateTimeField(auto_now=True)
    created_by = models.ForeignKey(User, on_delete=models.CASCADE)

    class Meta:
        db_table = 'client'
        indexes = [
            models.Index(fields=['dba'], name='cl_dba_idx'),
            models.Index(fields=['rfc'], name='cl_rfc_idx'),
        ]

    def __str__(self):
        return self.dba


class UserType(models.Model):
    name = models.CharField(max_length=20)

    class Meta:
        db_table = 'user_type'
        indexes = [
            models.Index(fields=['name'], name='usertype_name_idx')
        ]
    
    def __str__(self):
        return self.name


class CompanyHours(models.Model):
    date = models.DateField()
    start_hour = models.TimeField()
    end_hour = models.TimeField()

    class Meta:
        db_table = "company_hours"
        indexes = [
            models.Index(fields=['date'], name='company_hours_date_idx'),
            models.Index(fields=['start_hour'], name='company_hours_start_hour_idx'),
            models.Index(fields=['end_hour'], name='company_hours_end_hour_idx'),
        ]
    
    def __str__(self):
        return self.date


class EventSubtype(models.Model):
    name = models.CharField(max_length=50)

    class Meta:
        db_table = "event_subtype"
    
    def __str__(self):
        return self.name


class EventType(models.Model):
    name = models.CharField(max_length=50)
    subtype = models.ForeignKey(EventSubtype, null=True, on_delete=models.CASCADE)

    class Meta:
        db_table = "event_type"

    def __str__(self):
        return self.name + ' ' + self.subtype.name


class EventStatus(models.Model):
    name = models.CharField(max_length=20)
    color_class = models.CharField(max_length=30, default='none')
    color_class2 = models.CharField(max_length=30, default='none')

    class Meta:
        db_table = 'event_status'
        indexes = [
            models.Index(fields=['name'], name="event_status_name_idx")
        ]
    
    def __str__(self):
        return self.name


class Event(models.Model):
    event_type = models.ForeignKey(EventType, on_delete=models.CASCADE)
    client = models.ForeignKey(Client, on_delete=models.CASCADE)
    date = models.DateField()
    start_hour = models.TimeField()
    end_hour = models.TimeField()
    description = models.CharField(max_length=500)
    employees = models.ManyToManyField(User, related_name='employees')
    created_at = models.DateTimeField(auto_now=True)
    created_by = models.ForeignKey(User, on_delete=models.CASCADE)
    status = models.ForeignKey(EventStatus, on_delete=models.CASCADE, default=1, help_text="Optional Value default 1")
    observations = models.TextField(max_length=500, default='')

    class Meta:
        db_table = 'event'
        indexes = [
            models.Index(fields=['start_hour'], name='event_start_hour_idx'),
            models.Index(fields=['end_hour'], name='event_end_hour_idx'),
        ]
    
    def __str__(self):
        return self.client.dba + ' ' + str(self.start_hour) + ' ' + str(self.end_hour)


# class Profile(models.Model):
#     user = models.OneToOneField(User, on_delete=models.CASCADE)
#     user_type = models.ForeignKey(UserType, on_delete=models.CASCADE)


