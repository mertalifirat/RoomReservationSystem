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
            return redirect('shared_photo_library:home')
        return render(request, 'templates/login-page.html', {'form': form, 'user_authenticated': False})


class Logout(LoginRequiredMixin, View):
    def get(self, request):
        logout(request)
        return redirect('shared_photo_library:home')