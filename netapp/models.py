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