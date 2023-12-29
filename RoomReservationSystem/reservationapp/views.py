import json
from django import forms
from django.shortcuts import render
from django.db.models import Count, Q
from django.shortcuts import render, redirect
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth import login, logout
from django.views import View
from django.http import Http404, HttpResponse
from django.contrib.auth.mixins import LoginRequiredMixin
import pdb
from .classes.client import Client
from .models import *
from rest_framework.authtoken.models import Token
import socket
from . import constants

import os
from .forms import UserForm

clientManager = ClientManager()

class Login(View):
    def get(self, request):

        form = AuthenticationForm()
        print(request.user)
        return render(request, 'homepage.html', {'form': form})

    def post(self, request):
        form = AuthenticationForm(data=request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user)
            print("user logged in")
            user_id = request.user.id
            client = Client()
            clientManager.addClient(user_id, client)
            #pdb.set_trace()
            #Connect to phase2 server
            clientManager.getClient(user_id).connect()
            #Create request
            request = {
                "command": "LOGIN",
                "username": user.username,
                "password": user.password,
            }
            #Send request to phase2 server
            response = clientManager.getClient(user_id).make_request(request)
            #Receive response from phase2 server
            print(response)
            # Generate token
            token, created = Token.objects.get_or_create(user=user)
            print(created)
            response = redirect('reservationapp:home')
            # Set token as a cookie
            response.set_cookie('auth_token', token.key)
            return response
        return render(request, 'login-page.html', {'form': form, 'user_authenticated': False})


class Logout(LoginRequiredMixin, View):
    def get(self, request):
        logout(request)
        return redirect('reservationapp:home')
class Save(LoginRequiredMixin, View):
    def get(self,request):
        user = request.user
        user_authenticated = user.is_authenticated
        serverRequest = {
            "command": "SAVE",
        }
        clientManager.getClient(user.id).make_request(serverRequest)
        return render(request, 'homepage.html', {'user_authenticated': user_authenticated,})

class SignUp(View):
    def get(self, request):
        form = UserForm()
        return render(request, 'signup.html', {'form': form})

    def post(self, request):
        form = UserForm(request.POST)
        if form.is_valid():
            # pdb.set_trace()
            user = form.save(commit=False)
            #Conneting to the phase2 server
            password = form.cleaned_data['password1']
            user.set_password(password)  # Encrypt the password
            user.save()
            #pdb.set_trace()
            #Connection to request server port
            self.request_sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            self.request_sock.connect((constants.address, constants.request_port))
            print(form.cleaned_data['username'])
            request = {
                "command": "CREATE_USER",
                "django_id": user.id,
                "username": form.cleaned_data['username'],
                "email": form.cleaned_data['email'],
                "fullname": form.cleaned_data['first_name'],
                "password": user.password,
            }
            self.request_sock.send(str.encode(json.dumps(request)))
            server_response = self.request_sock.recv(4096).decode("utf8")
            self.request_sock.close()
            return redirect('reservationapp:login')
        return render(request, 'signup.html', {'form': form})



class Home(View):
    def get(self, request):
        user = request.user
        user_authenticated = user.is_authenticated
        form = AuthenticationForm()
        

        return render(request, 'homepage.html', {'form': form,
                                                 'user_authenticated': user_authenticated,})

class ListOrganizations(LoginRequiredMixin, View):
    def get(self, request):
        user = request.user
        user_authenticated = user.is_authenticated
        form = AuthenticationForm()
        #Create request
        serverRequest = {
            "command": "LIST_ORGANIZATIONS",
        }
        organizations = json.loads(clientManager.getClient(user.id).make_request(serverRequest))
        print(organizations)
        for org in organizations:
            Organization.objects.get_or_create(orgServerId = org["org_id"],orgName=org["org_name"], orgOwner=org["org_owner"])
        organizationCollections = list(Organization.objects.filter().only('orgName', 'orgOwner'))
        #pdb.set_trace()
        return render(request, 'homepage.html', {'form': form,
                                                 'user_authenticated': user_authenticated,
                                                 'organizations': organizationCollections})
    def post(self,request):
        user = request.user
        selectedOrgServerId = request.POST.get('orgServerId')
        selectedOrgName = request.POST.get('orgName')
        user_authenticated = user.is_authenticated
        #Create request
        serverRequest = {
            "command": "ATTACH_ORGANIZATION",
            "organization_id": request.POST.get('orgServerId'),
        }
        print(clientManager.getClient(user.id).make_request(serverRequest))
        #pdb.set_trace()
        return render(request, 'organization.html', {
                                                 'user_authenticated': user_authenticated,
                                                 'selectedOrgServerId': selectedOrgServerId,
                                                 'selectedOrgName': selectedOrgName,})
class OrganizationView(LoginRequiredMixin,View):
    def get(self,request):
        user = request.user
        user_authenticated = user.is_authenticated
        #print(request)
        form = AuthenticationForm()
        return render(request, 'organization.html', {'form': form,
                                                 'user_authenticated': user_authenticated,})
    def post(self,request):
        user = request.user
        selectedOrgServerId = request.POST.get('orgServerId')
        selectedOrgName = request.POST.get('orgName')
        user_authenticated = user.is_authenticated
        #Create request
        serverRequest = {
            "command": "LIST_ROOMS",
        }
        rooms = json.loads(clientManager.getClient(user.id).make_request(serverRequest))
        print(rooms)
        for room in rooms:
            #pdb.set_trace()
            Room.objects.get_or_create(roomId = room["room_id"],roomName=room["room_name"], roomCapacity=room["room_capacity"], roomWorkingHours=room["room_working_hours"])
        roomCollections = list(Room.objects.filter().only('roomName', 'roomCapacity', 'roomWorkingHours'))
        return render(request, 'organization.html', {
                                                 'user_authenticated': user_authenticated,
                                                 'selectedOrgServerId': selectedOrgServerId,
                                                 'selectedOrgName': selectedOrgName,
                                                 'rooms': roomCollections})
        

