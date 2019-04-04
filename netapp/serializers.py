from django.contrib.auth.models import User, Permission
from django_eventstream import send_event
from .models import Client, CompanyHours, EventSubtype, EventType, Event, EventStatus

from rest_framework import serializers
from rest_framework.renderers import JSONRenderer

import datetime as dt


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
            'available_permissions': {'read_only': True},
            'is_active': {'required': False}
            }
    
    def create(self, validated_data):
        request = self.context.get("request")
        user = User(
            username = validated_data['username'],
            email = validated_data['email'],
            first_name = validated_data['first_name'],
            last_name = validated_data['last_name'],
            is_active = validated_data['is_active']
        )
        user.set_password(validated_data['password'])
        user.save()
        serializer = UserSerializer(user)
        message = JSONRenderer().render(serializer.data)

        send_event('test', 'message', {
            'data': message.decode("utf-8"), 
            'notification': 'Nuevo usuario ' + user.username + ' creado por ' + request.user.username
            })
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
        serializer = UserSerializer(user)
        message = JSONRenderer().render(serializer.data)
        send_event('test', 'message', {
            'data': message.decode("utf-8"), 
            'notification': 'Modificación Permisos usuario '  + user.username + ' modificado por ' + request.user.username
            })
        return user


class CompanyHoursSerializer(serializers.ModelSerializer):
    slots = serializers.SerializerMethodField()

    class Meta:
        model = CompanyHours
        fields = ('id', 'date', 'start_hour', 'end_hour', 'slots')
        extra_kwargs = {
            'id': {'read_only': True},
            'date': {'required': True},
            'start_hour': {'required': True},
            'end_hour': {'required': True}
        }
    
    def get_events(self, obj):
        events = Event.objects.filter(date=obj.date)
        return events
    
    def get_slots(self, obj):
        result = []
        duration = obj.end_hour.hour - obj.start_hour.hour
        time_span = 1
        start = obj.start_hour
        events = self.get_events(obj)

        i = 0
        while i < duration:
            delta = dt.timedelta(hours = time_span)
            end = (dt.datetime.combine(dt.date(1,1,1), start) + delta).time()
            
            in_single_slot = events.filter(start_hour__gt=start, end_hour__lt=end)
            start_in_slot = events.filter(start_hour__lt=end, end_hour__gt=start).exclude(id__in=in_single_slot.values_list('id', flat=True))
            events_in_slots = in_single_slot | start_in_slot
            
            serializer = EventReadSerializer(events_in_slots, many=True)
            result.append({'start': start, 'end': end, 'events': serializer.data })
            start = end
            i += 1
        return result


class EventSubtypeSerializer(serializers.ModelSerializer):

    class Meta:
        model = EventSubtype
        fields = ('id', 'name')


class EventTypeSerializer(serializers.ModelSerializer):
    subtype = EventSubtypeSerializer(many=False)
    name = serializers.SerializerMethodField()

    class Meta:
        model = EventType
        fields = ('id', 'name', 'subtype')
    
    def get_name(self, obj):
        return obj.name + ' ' + obj.subtype.name


class EventSerializer(serializers.ModelSerializer):
    responsible_list = serializers.SerializerMethodField()

    class Meta:
        model = Event
        fields = ('id', 'date', 'start_hour', 'end_hour', 'description', 'created_at', 'created_by', 'responsible_list', 'event_type', 
                  'client', 'status', 'observations')
        extra_kwargs = {
            'id': {'read_only': True},
            'event_type': {'required': True},
            'client': {'required': True},
            'date': {'required': True},
            'start_hour': {'required': True},
            'end_hour': {'required': True},
            'description': {'required': True},
            'created_at': {'read_only': True},
            'created_by': {'read_only': True},
            'responsible_list': {'read_only': True},
            'status': {'required': False},
            'observations': {'required': False}
        }
    

    def create(self, validated_data):
        user = None
        request = self.context.get("request")
        employees = request.POST.get('employees', None)
        employees = employees.split(',')
        if request and hasattr(request, "user"):
            user = request.user
        event = Event(
            event_type = validated_data['event_type'],
            client = validated_data['client'],
            date = validated_data['date'], 
            start_hour = validated_data['start_hour'],
            end_hour = validated_data['end_hour'],
            description = validated_data['description'],
            created_by = user
        )
        event.save()
        for employee in employees:
            event.employees.add(int(employee))
        
        serializer = EventSerializer(event)
        message = JSONRenderer().render(serializer.data)
        send_event('test', 'message', {
                'data': message.decode("utf-8"), 
                'notification': 'Creación evento '  + str(event.id) + ' modificado por ' + request.user.username
                })
        return event

    def get_responsible_list(self, obj):
        data = obj.employees.all().values_list('username', flat=True)
        result = ','.join(str(e) for e in data)
        return result


class EventStatusSerializer(serializers.ModelSerializer):
    class Meta:
        model = EventStatus
        fields = ('id', 'name', 'color_class', 'color_class2')


class EventReadSerializer(EventSerializer):
    event_type = EventTypeSerializer(many=False, read_only=True)
    client = ClientSerializer(many=False, read_only=True)
    employees = UserSerializer(many=True, read_only=True)
    created_by = UserSerializer(many=False, read_only=True)
    status = EventStatusSerializer(many=False, read_only=True)

    class Meta:
        model = Event
        fields = ('id', 'date', 'start_hour', 'end_hour', 'description', 'created_at', 'created_by', 'responsible_list', 'event_type', 
                  'client', 'employees', 'status', 'observations')