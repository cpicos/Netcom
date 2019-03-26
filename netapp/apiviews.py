from django.contrib.auth.models import User, Permission
from django.contrib.auth import authenticate, login, logout
from django.http import Http404
from django.http import HttpResponseRedirect
from django.shortcuts import render_to_response, redirect

from rest_framework import generics, status, viewsets, permissions
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.renderers import JSONRenderer

import datetime as dt
from datetime import timedelta 

from django_eventstream import send_event

from .models import Client, CompanyHours
from .serializers import UserSerializer, ClientSerializer, UserPermissionSerializer, CompanyHoursSerializer


class LoginView(APIView):
    template_name = "login.html"
    permission_classes = ()

    def get(self, request, ):
        if request.user is not None:
            if request.user.is_active:
                return HttpResponseRedirect('/home/')
            else:
                return render_to_response('login.html')
        else:
            return render_to_response('login.html')

    def post(self, request, ):
        username = request.data.get("username")
        password = request.data.get("password")
        user = authenticate(username=username, password=password)
        if user is not None:
            login(request, user)
            return HttpResponseRedirect('/home/')
        else:
            return render_to_response('login.html', {'error': 'Usuario/Contraseña Incorrectos'})


class LogoutView(APIView):
    permission_classes = (permissions.IsAuthenticated,)

    def get(self, request, ):
        logout(request)
        return redirect('login')


class UserViewSet(viewsets.ModelViewSet):
    permission_classes = (permissions.IsAuthenticated, permissions.DjangoModelPermissions)
    queryset = User.objects.all()
    serializer_class = UserSerializer

    def partial_update(self, request, *args, **kwargs):
        # print(request)
        response = super(UserViewSet, self).partial_update(request, *args, **kwargs)
        user = self.get_object()
        serializer = UserSerializer(user)
        message = JSONRenderer().render(serializer.data)
        send_event('test', 'message', {
            'data': message.decode("utf-8"), 
            'notification': 'Actialización usuario '  + user.username + ' modificado por ' + request.user.username
            })
        return response
    

    def destroy(self, request, *args, **kwargs):
        print('HELLO MAKING DESTROY!!')
        user = self.get_object()
        username = user.username
        send_event('test', 'message', {
            'data': 'DELETE', 
            'id': user.id,
            'notification': 'Actialización usuario '  + username + ' modificado por ' + request.user.username
            })
        super(UserViewSet, self).destroy(request, *args, **kwargs)
        return Response(status=status.HTTP_204_NO_CONTENT)

        
class ClientViewSet(viewsets.ModelViewSet):
    permission_classes = (permissions.IsAuthenticated, permissions.DjangoModelPermissions)
    queryset = Client.objects.all()
    serializer_class = ClientSerializer


class UserPermViewSet(viewsets.ModelViewSet):
    permission_classes = (permissions.IsAuthenticated, permissions.DjangoModelPermissions)
    queryset = User.objects.all()
    serializer_class = UserPermissionSerializer


    def partial_update(self, request, *args, **kwargs):
        request = self.request
        user_id = request.POST.get('user_id')
        perm_id = request.POST.get('perm_id')
        user = User.objects.get(id=user_id)
        permission = Permission.objects.get(id=perm_id)
        user.user_permissions.remove(permission)
        serializer = UserPermissionSerializer(user)
        message = JSONRenderer().render(serializer.data)
        send_event('test', 'message', {
            'data': message.decode("utf-8"), 
            'notification': 'Modificación Permisos usuario '  + user.username + ' modificado por ' + request.user.username
            })
        return Response(serializer.data, status=status.HTTP_200_OK)


class CompanyHoursViewSet(viewsets.ModelViewSet):
    permission_classes = (permissions.IsAuthenticated, permissions.DjangoModelPermissions)
    queryset = CompanyHours.objects.all()
    serializer_class = CompanyHoursSerializer

    def get_queryset(self):
        start = self.request.GET.get('start_date')
        start = dt.datetime.strptime(start, "%Y-%m-%d").date()
        end = start + timedelta(days=6)
        return CompanyHours.objects.filter(date__range=[start, end])
