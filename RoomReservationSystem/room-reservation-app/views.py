from django.shortcuts import render
from django.db.models import Count, Q
from django.shortcuts import render, redirect
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth import login, logout
from django.views import View
from django.http import Http404, HttpResponse
from django.contrib.auth.mixins import LoginRequiredMixin
from .models import *

import os
class Login(View):
    def get(self, request):

        form = AuthenticationForm()
        
        return render(request, 'homepage.html', {'form': form})

    def post(self, request):
        form = AuthenticationForm(data=request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user)
            print("user  logged in")
            return redirect('room-reservation-app:home')
        return render(request, 'templates/login-page.html', {'form': form, 'user_authenticated': False})


class Logout(LoginRequiredMixin, View):
    def get(self, request):
        logout(request)
        return redirect('room-reservation-app:home')

class SignUp(View):
    def get(self, request):
        form = UserCreationForm()
        return render(request, 'signup.html', {'form': form})

    def post(self, request):
        form = UserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('room-reservation-app:login')
        return render(request, 'signup.html', {'form': form})



class Home(View):
    def get(self, request):
        user = request.user
        user_authenticated = user.is_authenticated
        form = AuthenticationForm()
        

        return render(request, 'homepage.html', {'form': form,
                                                 'user_authenticated': user_authenticated,})
