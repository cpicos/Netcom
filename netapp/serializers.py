from django.contrib.auth.models import User, Permission
from .models import Client

from rest_framework import serializers


class UserSerializer(serializers.ModelSerializer):
    available_permissions = serializers.SerializerMethodField()
    
    class Meta:
        model = User
        fields = ('id', 'username', 'email', 'password', 'first_name', 'last_name', 'is_active', 'available_permissions')
        extra_kwargs = {
            'id': {'read_only': True},
            'username': {'required': True},
            'email': {'required': True},
            'first_name': {'required': True},
            'last_name': {'required': True},
            'password': {'write_only': True, 'required': True},
            'available_permissions': {'read_only': True}
            }
    
    def create(self, validated_data):
        user = User(
            username = validated_data['username'],
            email = validated_data['email'],
            first_name = validated_data['first_name'],
            last_name = validated_data['last_name'],
            is_active = validated_data['is_active']
        )
        user.set_password(validated_data['password'])
        user.save()
        return user
    
    def get_chosen_permissions(self, obj):
        permissions = Permission.objects.filter(user=obj, content_type__app_label__in=['netapp', 'auth'])
        permissions = permissions.exclude(content_type__id__in=(2, 3)).values_list('id', flat=True)
        return permissions
    
    def get_available_permissions(self, obj):
        permissions = Permission.objects.filter(content_type__app_label__in=['netapp', 'auth'])
        permissions = permissions.exclude(content_type__id__in=(2, 3)).values('id', 'codename').values('id', 'codename')
        chosen_permissions = self.get_chosen_permissions(obj)
        
        for perm in permissions:
            if perm['id'] in chosen_permissions:
                perm['chosen'] = True
            else:
                perm['chosen'] = False
        return permissions
    
    
class ClientSerializer(serializers.ModelSerializer):

    class Meta:
        model = Client
        fields = ('id', 'name', 'dba', 'rfc', 'address', 'postal_code', 'created_at', 'created_by') 
        extra_kwargs = {
            'id': {'read_only': True},
            'name': {'required': True},
            'dba': {'required': True},
            'rfc': {'required': True},
            'address': {'required': True},
            'postal_code': {'required': True},
            'created_at': {'read_only': True},
            'created_by': {'read_only': True}
        }
    
    def create(self, validated_data):
        user = None
        request = self.context.get("request")
        if request and hasattr(request, "user"):
            user = request.user

        client = Client(
            name = validated_data['name'],
            dba = validated_data['dba'],
            rfc = validated_data['rfc'],
            address = validated_data['address'],
            postal_code = validated_data['postal_code'],
            created_by = user
        )
        client.save()
        return client


class UserPermissionSerializer(serializers.ModelSerializer):
    available_permissions = serializers.SerializerMethodField()

    class Meta:
        model = User
        fields = ('id', 'available_permissions')
    

    def get_chosen_permissions(self, obj):
        permissions = Permission.objects.filter(user=obj, content_type__app_label__in=['netapp', 'auth'])
        permissions = permissions.exclude(content_type__id__in=(2, 3)).values_list('id', flat=True)
        return permissions
    

    def get_available_permissions(self, obj):
        permissions = Permission.objects.filter(content_type__app_label__in=['netapp', 'auth'])
        permissions = permissions.exclude(content_type__id__in=(2, 3)).values('id', 'codename').values('id', 'codename')
        chosen_permissions = self.get_chosen_permissions(obj)
        
        for perm in permissions:
            if perm['id'] in chosen_permissions:
                perm['chosen'] = True
            else:
                perm['chosen'] = False
        return permissions


    def create(self, validated_data):
        request = self.context.get("request")
        user_id = request.POST.get('user_id')
        perm_id = request.POST.get('perm_id')
        user = User.objects.get(id=user_id)
        permission = Permission.objects.get(id=perm_id)
        user.user_permissions.add(permission)
        return user
