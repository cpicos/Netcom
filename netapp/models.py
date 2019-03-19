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
        permissions = (
            ('can_add_client', 'can_add_client'),
            ('can_change_client', 'can_change_client'),
            ('can_delete_client', 'can_delete_client'),
            ('can_view_client', 'can_view_client'),
        )
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


class User1(User):
    # Extending auth user model without creating other table this is for adding permissions
    class Meta:
        proxy = True
        permissions = (
            ('can_add_user', 'can_add_user'),
            ('can_change_user', 'can_change_user'),
            ('can_delete_user', 'can_delete_user'),
            ('can_view_user', 'can_view_user'),
        )


# class Profile(models.Model):
#     user = models.OneToOneField(User, on_delete=models.CASCADE)
#     user_type = models.ForeignKey(UserType, on_delete=models.CASCADE)


