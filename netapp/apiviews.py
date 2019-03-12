from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout
from django.http import Http404
from django.http import HttpResponseRedirect
from django.shortcuts import render_to_response, redirect

from rest_framework import generics, status, viewsets, permissions
from rest_framework.views import APIView
from rest_framework.response import Response

from .serializers import UserSerializer


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
    permission_classes = ()

    def get(self, request, ):
        logout(request)
        return redirect('login')


class UserViewSet(viewsets.ModelViewSet):
    permission_classes = (permissions.IsAuthenticated,)
    queryset = User.objects.all()
    serializer_class = UserSerializer