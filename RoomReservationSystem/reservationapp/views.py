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
from datetime import datetime

import os
from .forms import EventForm, QueryForm, RoomForm, UserForm

clientManager = ClientManager()


class Login(View):
    def get(self, request):
        form = AuthenticationForm()
        print(request.user)
        return render(request, "homepage.html", {"form": form})

    def post(self, request):
        form = AuthenticationForm(data=request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user)
            print("user logged in")
            user_id = request.user.id
            client = Client()
            clientManager.addClient(user_id, client)
            # pdb.set_trace()
            # Connect to phase2 server
            clientManager.getClient(user_id).connect()
            # Create request
            request = {
                "command": "LOGIN",
                "username": user.username,
                "password": user.password,
            }
            # Send request to phase2 server
            response = clientManager.getClient(user_id).make_request(request)
            # Receive response from phase2 server
            print(response)
            # Generate token
            token, created = Token.objects.get_or_create(user=user)
            print(created)
            response = redirect("reservationapp:home")
            # Set token as a cookie
            response.set_cookie("auth_token", token.key)
            return response
        return render(
            request, "login-page.html", {"form": form, "user_authenticated": False}
        )


class Logout(LoginRequiredMixin, View):
    def get(self, request):
        logout(request)
        return redirect("reservationapp:home")


class Save(LoginRequiredMixin, View):
    def get(self, request):
        user = request.user
        user_authenticated = user.is_authenticated
        serverRequest = {
            "command": "SAVE",
        }
        clientManager.getClient(user.id).make_request(serverRequest)
        return render(
            request,
            "homepage.html",
            {
                "user_authenticated": user_authenticated,
            },
        )


class SignUp(View):
    def get(self, request):
        form = UserForm()
        return render(request, "signup.html", {"form": form})

    def post(self, request):
        form = UserForm(request.POST)
        if form.is_valid():
            # pdb.set_trace()
            user = form.save(commit=False)
            # Conneting to the phase2 server
            password = form.cleaned_data["password1"]
            user.set_password(password)  # Encrypt the password
            user.save()
            # pdb.set_trace()
            # Connection to request server port
            self.request_sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            self.request_sock.connect((constants.address, constants.request_port))
            print(form.cleaned_data["username"])
            request = {
                "command": "CREATE_USER",
                "django_id": user.id,
                "username": form.cleaned_data["username"],
                "email": form.cleaned_data["email"],
                "fullname": form.cleaned_data["first_name"],
                "password": user.password,
            }
            self.request_sock.send(str.encode(json.dumps(request)))
            server_response = self.request_sock.recv(4096).decode("utf8")
            self.request_sock.close()
            return redirect("reservationapp:login")
        return render(request, "signup.html", {"form": form})


class Home(View):
    def get(self, request):
        user = request.user
        user_authenticated = user.is_authenticated
        form = AuthenticationForm()

        return render(
            request,
            "homepage.html",
            {
                "form": form,
                "user_authenticated": user_authenticated,
            },
        )


class ListOrganizations(LoginRequiredMixin, View):
    def get(self, request):
        user = request.user
        user_authenticated = user.is_authenticated
        form = AuthenticationForm()
        print(request)
        # Create request
        serverRequest = {
            "command": "LIST_ORGANIZATIONS",
        }
        organizations = json.loads(
            clientManager.getClient(user.id).make_request(serverRequest)
        )
        print(organizations)
        # pdb.set_trace()
        return render(
            request,
            "homepage.html",
            {
                "form": form,
                "user_authenticated": user_authenticated,
                "organizations": organizations,
            },
        )

    def post(self, request):
        user = request.user
        selectedOrgServerId = request.POST.get("orgServerId")
        selectedOrgName = request.POST.get("orgName")
        user_authenticated = user.is_authenticated
        form = RoomForm()
        # Create request
        serverRequest = {
            "command": "ATTACH_ORGANIZATION",
            "organization_id": request.POST.get("orgServerId"),
        }
        print(clientManager.getClient(user.id).make_request(serverRequest))
        # pdb.set_trace()
        return render(
            request,
            "organization.html",
            {
                "user_authenticated": user_authenticated,
                "form": form,
                "selectedOrgId": selectedOrgServerId,
                "selectedOrgName": selectedOrgName,
            },
        )


class OrganizationView(LoginRequiredMixin, View):
    def get(self, request):
        user = request.user
        user_authenticated = user.is_authenticated
        selectedOrgServerId = request.GET.get("orgServerId")
        selectedOrgName = request.GET.get("orgName")
        # print(request)
        return render(
            request,
            "organization.html",
            {
                "user_authenticated": user_authenticated,
                "selectedOrgServerId": selectedOrgServerId,
                "selectedOrgName": selectedOrgName,
            },
        )

    def post(self, request):
        user = request.user
        selectedOrgServerId = request.POST.get("orgServerId")
        selectedOrgName = request.POST.get("orgName")
        user_authenticated = user.is_authenticated
        
        if request.POST.get("deleteRoom"):
            # Create request
            print(request.POST.get("roomServerId"))
            serverRequest = {
                "command": "DELETE_ROOM",
                "room_id": request.POST.get("roomServerId"),
            }
            print(clientManager.getClient(user.id).make_request(serverRequest))
            Room.objects.filter(roomId=request.POST.get("roomServerId")).delete()
            form = RoomForm()
            return render(
                request,
                "organization.html",
                {
                    "form": form,
                    "user_authenticated": user_authenticated,
                    "selectedOrgServerId": selectedOrgServerId,
                    "selectedOrgName": selectedOrgName,
                },
            )
        if request.POST.get("addRoom"):
            # Create request
            form = RoomForm(request.POST)
            # pdb.set_trace()

            if form.is_valid():
                serverRequest = {
                    "command": "ADD_ROOM",
                    "room_name": form.cleaned_data["roomName"],
                    "room_capacity": form.cleaned_data["roomCapacity"],
                    "room_working_hours": form.cleaned_data["roomWorkingHours"],
                    "room_permissions": form.cleaned_data["roomPermissions"],
                }
                print(clientManager.getClient(user.id).make_request(serverRequest))
                form = RoomForm()
                return render(
                    request,
                    "organization.html",
                    {
                        "form": form,
                        "user_authenticated": user_authenticated,
                        "selectedOrgServerId": selectedOrgServerId,
                        "selectedOrgName": selectedOrgName,
                    },
                )
        if request.POST.get("showRoom"):
            # Go to room page
            selectedRoomId = request.POST.get("roomServerId")
            selectedRoomName = request.POST.get("roomName")
            selectedOrgServerId = request.POST.get("orgServerId")
            selectedOrgName = request.POST.get("orgName")
            form = EventForm()
            return render(
                request,
                "room.html",
                {
                    "form": form,
                    "user_authenticated": user_authenticated,
                    "selectedOrgServerId": selectedOrgServerId,
                    "selectedOrgName": selectedOrgName,
                    "selectedRoomServerId": selectedRoomId,
                    "selectedRoomName": selectedRoomName,
                },
            )


class MapView(LoginRequiredMixin, View):
    def get(self, request):
        user = request.user
        user_authenticated = user.is_authenticated
        selectedOrgServerId = request.GET.get("orgServerId")
        selectedOrgName = request.GET.get("orgName")
        serverRequest = {
            "command": "LIST_ROOMS",
        }
        rooms = json.loads(clientManager.getClient(user.id).make_request(serverRequest))
        # print(rooms)
        roomCoordinates = []
        for room in rooms:
            # pdb.set_trace()
            Room.objects.get_or_create(
                roomId=room["room_id"],
                roomName=room["room_name"],
                roomCapacity=room["room_capacity"],
                roomWorkingHours=room["room_working_hours"],
            )
            roomCoordinates.append(
                (
                    room["room_name"],
                    room["room_id"],
                    room["room_x"],
                    room["room_y"],
                    room["room_capacity"],
                    room["room_working_hours"],
                )
            )
        roomCollections = list(
            Room.objects.filter().only(
                "roomId", "roomName", "roomCapacity", "roomWorkingHours"
            )
        )
        return render(
            request,
            "map.html",
            {
                "user_authenticated": user_authenticated,
                "selectedOrgServerId": selectedOrgServerId,
                "selectedOrgName": selectedOrgName,
                "roomCollections": roomCollections,
                "roomCoordinates": roomCoordinates,
            },
        )


class AddRoomView(LoginRequiredMixin, View):
    def get(self, request):
        user = request.user
        user_authenticated = user.is_authenticated
        # pdb.set_trace()
        if request.GET.get("addRoom"):
            selectedOrgServerId = request.GET.get("orgServerId")
            selectedOrgName = request.GET.get("orgName")

            x = request.GET.get("x")
            y = request.GET.get("y")
            print(x, y)
            form = RoomForm(initial={"x": x, "y": y})
            return render(
                request,
                "add-room-page.html",
                {
                    "form": form,
                    "user_authenticated": user_authenticated,
                    "selectedOrgServerId": selectedOrgServerId,
                    "selectedOrgName": selectedOrgName,
                },
            )

    def post(self, request):
        user = request.user
        user_authenticated = user.is_authenticated
        selectedOrgServerId = request.POST.get("orgServerId")
        selectedOrgName = request.POST.get("orgName")
        # Create request
        form = RoomForm(request.POST)
        pdb.set_trace()
        if form.is_valid():
            serverRequest = {
                "command": "ADD_ROOM",
                "room_name": form.cleaned_data["roomName"],
                "room_capacity": form.cleaned_data["roomCapacity"],
                "room_working_hours": form.cleaned_data["roomWorkingHours"],
                "room_permissions": form.cleaned_data["roomPermissions"],
                "room_x": form.cleaned_data["x"],
                "room_y": form.cleaned_data["y"],
            }
            print(clientManager.getClient(user.id).make_request(serverRequest))

            return redirect("reservationapp:map")
            # return render(
            #     request,
            #     "map.html",
            #     {
            #         "user_authenticated": user_authenticated,
            #         "selectedOrgServerId": selectedOrgServerId,
            #         "selectedOrgName": selectedOrgName,
            #     },
            # )


class roomView(LoginRequiredMixin, View):
    def get(self, request):
        user = request.user
        user_authenticated = user.is_authenticated
        selectedRoomServerId = request.GET.get("roomServerId")
        selectedRoomName = request.GET.get("roomName")
        selectedOrgServerId = request.GET.get("orgServerId")
        selectedOrgName = request.GET.get("orgName")
        form = EventForm()
        client_notification_port = clientManager.getClient(user.id).notification_port
        # print(request)
        return render(
            request,
            "room.html",
            {
                "user_authenticated": user_authenticated,
                "form": form,
                "selectedOrgServerId": selectedOrgServerId,
                "selectedOrgName": selectedOrgName,
                "selectedRoomServerId": selectedRoomServerId,
                "selectedRoomName": selectedRoomName,
                "client_notification_port": client_notification_port,
            },
        )

    def post(self, request):
        user = request.user
        user_authenticated = user.is_authenticated
        selectedOrgServerId = request.POST.get("orgServerId")
        selectedOrgName = request.POST.get("orgName")
        selectedRoomServerId = request.POST.get("roomServerId")
        selectedRoomName = request.POST.get("roomName")
        #pdb.set_trace()
        if request.POST.get("listReservedEvents"):
            # Create request
            serverRequest = {
                "command": "LIST_RESERVED_EVENTS",
                "room_id": selectedRoomServerId,
            }
            events = json.loads(
                clientManager.getClient(user.id).make_request(serverRequest)
            )
            eventHours = {}
            form = EventForm()
            return render(
                request,
                "room.html",
                {
                    "user_authenticated": user_authenticated,
                    "form": form,
                    "selectedOrgServerId": selectedOrgServerId,
                    "selectedOrgName": selectedOrgName,
                    "selectedRoomServerId": selectedRoomServerId,
                    "selectedRoomName": selectedRoomName,
                    "events": events,
                    "eventHours": eventHours,
                },
            )
        if request.POST.get("reserveRoom"):
            form = EventForm(request.POST)
            # pdb.set_trace()
            # Create request
            if form.is_valid():
                serverRequest = {
                    "command": "RESERVE",
                    "room_id": selectedRoomServerId,
                    "event_title": form.cleaned_data["eventTitle"],
                    "event_category": form.cleaned_data["eventCategory"],
                    "event_description": form.cleaned_data["eventDescription"],
                    "event_capacity": form.cleaned_data["eventCapacity"],
                    "event_duration": form.cleaned_data["eventDuration"],
                    "event_weekly": form.cleaned_data["eventWeekly"],
                    "event_permissions": form.cleaned_data["eventPermissions"],
                    "event_start": form.cleaned_data["eventStart"],
                }
                message = clientManager.getClient(user.id).make_request(serverRequest)
                form = EventForm()
                return render(
                    request,
                    "room.html",
                    {
                        "user_authenticated": user_authenticated,
                        "form": form,
                        "selectedOrgServerId": selectedOrgServerId,
                        "selectedOrgName": selectedOrgName,
                        "selectedRoomServerId": selectedRoomServerId,
                        "selectedRoomName": selectedRoomName,
                        "message": message,
                    },
                )
        if request.POST.get("deleteReservation"):
            # Create request
            eventHours = request.POST.get("eventHours")
            print(eventHours)
            eventHours = eventHours.split(" - ")
            print(eventHours)
            eventStart = datetime.strptime(eventHours[0], "%Y-%m-%d %H:%M:%S")
            eventEnd = datetime.strptime(eventHours[1], "%Y-%m-%d %H:%M:%S")
            eventStart = eventStart.strftime("%Y-%m-%d-%H:%M")
            eventEnd = eventEnd.strftime("%Y-%m-%d-%H:%M")
            print(eventStart)
            print(eventEnd)
            serverRequest = {
                "command": "DELETE_RESERVATION",
                "room_id": selectedRoomServerId,
                "event_id": request.POST.get("eventServerId"),
                "event_start": eventStart,
                "event_end": eventEnd,
            }
            print(clientManager.getClient(user.id).make_request(serverRequest))
            Event.objects.filter(eventId=request.POST.get("eventServerId")).delete()
            form = EventForm()
            return render(
                request,
                "room.html",
                {
                    "user_authenticated": user_authenticated,
                    "form": form,
                    "selectedOrgServerId": selectedOrgServerId,
                    "selectedOrgName": selectedOrgName,
                    "selectedRoomServerId": selectedRoomServerId,
                    "selectedRoomName": selectedRoomName,
                },
            )


class EventView(LoginRequiredMixin, View):
    def get(self, request):
        user = request.user
        user_authenticated = user.is_authenticated
        selectedOrgServerId = request.GET.get("orgServerId")
        selectedOrgName = request.GET.get("orgName")
        form = QueryForm()
        return render(
            request,
            "event.html",
            {
                "user_authenticated": user_authenticated,
                "selectedOrgServerId": selectedOrgServerId,
                "selectedOrgName": selectedOrgName,
                "form": form,
            },
        )

    def post(self, request):
        user = request.user
        user_authenticated = user.is_authenticated
        selectedOrgServerId = request.POST.get("orgServerId")
        selectedOrgName = request.POST.get("orgName")
        form = QueryForm(request.POST)

        if form.is_valid():
            # Create request
            rect = (
                form.cleaned_data["X1"],
                form.cleaned_data["Y1"],
                form.cleaned_data["X2"],
                form.cleaned_data["Y2"],
            )
            serverRequest = {
                "command": "QUERY",
                "rect": rect,
                "title": form.cleaned_data["title"],
                "category": form.cleaned_data["category"],
                "room": form.cleaned_data["room"],
            }
            # list of tuples (event,room,start)
            queryResult = json.loads(
                clientManager.getClient(user.id).make_request(serverRequest)
            )
            print(queryResult)
            form = QueryForm()
            return render(
                request,
                "event.html",
                {
                    "user_authenticated": user_authenticated,
                    "form": form,
                    "selectedOrgServerId": selectedOrgServerId,
                    "selectedOrgName": selectedOrgName,
                    "queryResult": queryResult,
                },
            )


class DayView(LoginRequiredMixin, View):
    def get(self, request):
        user = request.user
        user_authenticated = user.is_authenticated
        selectedOrgServerId = request.GET.get("orgServerId")
        selectedOrgName = request.GET.get("orgName")
        return render(
            request,
            "dayView.html",
            {
                "user_authenticated": user_authenticated,
                "selectedOrgServerId": selectedOrgServerId,
                "selectedOrgName": selectedOrgName,
            },
        )

    def post(self, request):
        user = request.user
        user_authenticated = user.is_authenticated
        selectedOrgServerId = request.POST.get("orgServerId")
        selectedOrgName = request.POST.get("orgName")
        # Create request
        serverRequest = {
            "command": "DAY_VIEW",
        }
        pdb.set_trace()
        dayViewResult = json.loads(
            clientManager.getClient(user.id).make_request(serverRequest)
        )
        print(dayViewResult)
        return render(
            request,
            "dayView.html",
            {
                "user_authenticated": user_authenticated,
                "selectedOrgServerId": selectedOrgServerId,
                "selectedOrgName": selectedOrgName,
                "events": dayViewResult,
            },
        )


class RoomView(LoginRequiredMixin, View):
    def get(self, request):
        user = request.user
        user_authenticated = user.is_authenticated
        selectedOrgServerId = request.GET.get("orgServerId")
        selectedOrgName = request.GET.get("orgName")
        return render(
            request,
            "roomView.html",
            {
                "user_authenticated": user_authenticated,
                "selectedOrgServerId": selectedOrgServerId,
                "selectedOrgName": selectedOrgName,
            },
        )

    def post(self, request):
        user = request.user
        user_authenticated = user.is_authenticated
        selectedOrgServerId = request.POST.get("orgServerId")
        selectedOrgName = request.POST.get("orgName")
        # Create request
        serverRequest = {
            "command": "ROOM_VIEW",
        }
        roomViewResult = json.loads(
            clientManager.getClient(user.id).make_request(serverRequest)
        )
        print(roomViewResult)
        return render(
            request,
            "roomView.html",
            {
                "user_authenticated": user_authenticated,
                "selectedOrgServerId": selectedOrgServerId,
                "selectedOrgName": selectedOrgName,
                "events": roomViewResult,
            },
        )
