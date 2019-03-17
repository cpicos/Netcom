from django.contrib.auth.models import User
from .models import Client

from rest_framework import serializers


class UserSerializer(serializers.ModelSerializer):
    
    class Meta:
        model = User
        fields = ('id', 'username', 'email', 'password', 'first_name', 'last_name', 'is_active')
        extra_kwargs = {
            'id': {'read_only': True},
            'username': {'required': True},
            'email': {'required': True},
            'first_name': {'required': True},
            'last_name': {'required': True},
            'password': {'write_only': True, 'required': True} 
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
