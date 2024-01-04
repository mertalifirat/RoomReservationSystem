
from threading import Thread, Lock, Condition
import socket
import sys
import sqlite3
import json
from json import JSONDecodeError

import websockets
from database import Database
from room import Room
from event import Event
from user import User
import hashlib
import pickle
import pdb
import asyncio
from datetime import datetime
from singletonCatalgoue import Catalogue
import uuid
from websockets.sync import server
from websockets.exceptions  import ConnectionClosedOK, ConnectionClosedError
HOST = "127.0.0.1"
PORT = 1422

async def RequestAgent(sock):
    mutex = Lock()
    organization_and_user_list= Catalogue()
    userList = {}
    request_port = request_port
    notification_port = notification_port
    pdb.set_trace()
    sockected_clients = 0
    sql_db = sqlite3.sockect("database.db", check_same_thread=False)
    try:
        organization_and_user_list = pickle.load(open("organizations.p","rb"))
        print(organization_and_user_list.getOrganizationList().keys())
        print(organization_and_user_list.getUserList().keys())
    except FileNotFoundError as err:
        print("error:" + str(err))
            
    db = Database(sql_db, sql_db.cursor())

    try:
        while True:
            inp = await sock.recv()
            
            print("in server",inp,"\n")
            decode8 = inp.decode("utf8")
            try:
                request = json.loads(decode8)
            except JSONDecodeError:
                notexit = False

            request_type = request["command"]
            request["user_id"] = client_user_id

            if request_type == "CREATE_USER":  # CREATE_USER
                with mutex:
                   

                    user = User(
                        request["username"],
                        request["email"],
                        request["fullname"],
                        request["password"],
                    )
                    
                    user_id = str(user.getId())
                    django_id = request["django_id"]

                    #Add user to catalogue
                    organization_and_user_list.addUser(user)

                    db.insert(
                        "Users",
                        ("django_id","user_id", "username", "email", "fullname", "password"),
                        django_id,
                        user_id,
                        user.get_username(),
                        user.get_email(),
                        user.get_fullname(),
                        user.get_passwd(),
                    )
                    
                    print("Server: User created successfully.")
                    await sock.send(str.encode(user.get_fullname()))

            elif request_type == "LOGIN": #LOGIN
                with mutex:
                    print(request)
                    username = request["username"]
                    encoded_password = request["password"]

                    c = db.curs
                    
                    row = c.execute(
                        f"SELECT user_id, password FROM Users WHERE username = '{username}'"
                    ).fetchone()

                    if encoded_password == row[1]:
                        print("Login successful")
                        client_user_id = uuid.UUID(row[0])
                        #print(client_user_id)
                        await sock.send("Login successful".encode("utf8"))
                    else:
                        print("Login failed")
                        await sock.send("Login failed".encode("utf8"))


            #Organization operations
            elif request_type ==  "LIST_ORGANIZATIONS": #List organizations
                with mutex:
                    result = []
                    if client_user_id is not None:
                        for organization in organization_and_user_list.getOrganizationList().values():
                            result.append(organization.getOrganizationInfo())
                        await sock.send(str.encode(json.dumps(result)))
                    else:
                        await sock.send("Not authorized, please login".encode("utf8"))    
            
            elif request_type == "ATTACH_ORGANIZATION": #Attaching organization to user
                with mutex:
                    if client_user_id is not None:
                        organization_id = uuid.UUID(request["organization_id"])
                        user = organization_and_user_list.getUser(client_user_id)
                        user.update_attachedOrganization(organization_id)
                        await sock.send(str.encode("Organization attached"))
                    else:
                        await sock.send("Not authorized, please login".encode("utf8"))

            elif request_type == "DETACH_ORGANIZATION": #Attaching organization to user
                with mutex:
                    if client_user_id is not None:
                        user = organization_and_user_list.getUser(client_user_id)
                        user.update_attachedOrganization(None)
                        await sock.send(str.encode("Organization detached"))
                    else:
                        await sock.send("Not authorized, please login".encode("utf8"))            

            elif request_type == "LIST_ROOMS": #Listing rooms
                with mutex:
                    if client_user_id is not None:
                        organization_id = organization_and_user_list.getUser(client_user_id).get_attachedOrganization()
                        if organization_id is None:
                            await sock.send("Please attach to an organization first".encode("utf8"))
                        else:    
                            org = organization_and_user_list.getOrganization(organization_id)
                            #Check if user has permission to list rooms
                            # pdb.set_trace()
                            if "LIST" in org.getUserPermissions(client_user_id):
                                await sock.send(str.encode(json.dumps(org.listRooms())))
                            else:
                                await sock.send("You don't have access for listing the rooms".encode("utf8"))    
                    else:
                        await sock.send("Not authorized, please login".encode("utf8"))

            elif request_type == "ADD_ROOM": #Adding room
                with mutex:
                    if client_user_id is not None:
                        organization_id = organization_and_user_list.getUser(client_user_id).get_attachedOrganization()
                        if organization_id is None:
                            await sock.send("Please attach to an organization first".encode("utf8"))
                        else:    
                            org = organization_and_user_list.getOrganization(organization_id)
                            #Check if user has permission to add rooms
                            if "ADD" in org.getUserPermissions(client_user_id):
                                #pdb.set_trace()
                                start_end = request["room_working_hours"].split("-")
                                start = datetime.strptime(start_end[0], "%H:%M").time()
                                end = datetime.strptime(start_end[1], "%H:%M").time()
                                working_hours = (start,end)
                                #Make permissions dictionary with {userId:[PERMISSIONS]}
                                permissions = { client_user_id :request["room_permissions"]}
                                room = Room(request["room_name"],0,0,int(request["room_capacity"]),working_hours,permissions)
                                org.addRoom(room)
                                await sock.send(str.encode("Room added"))
                            else:
                                await sock.send("You don't have access for adding rooms".encode("utf8"))    
                    else:
                        await sock.send("Not authorized, please login".encode("utf8"))

            elif request_type == "ACCESS": #Accessing rooms and events
                with mutex:
                    if client_user_id is not None:
                        organization_id = organization_and_user_list.getUser(client_user_id).get_attachedOrganization()
                        if organization_id is None:
                            await sock.send("Please attach to an organization first".encode("utf8"))
                        else:    
                            org = organization_and_user_list.getOrganization(organization_id)
                            if "ACCESS" in org.getUserPermissions(client_user_id):
                                await sock.sendall(str.encode(org.accessRoomsandEvents()))
                            else:
                                await sock.send("You don't have access for accessing rooms and events".encode("utf8"))
                    else:
                        await sock.send("Not authorized, please login".encode("utf8"))

            #Room operations
            elif request_type == "DELETE_ROOM": #Deleting room
                with mutex:
                    if client_user_id is not None:
                        organization_id = organization_and_user_list.getUser(client_user_id).get_attachedOrganization()
                        if organization_id is None:
                            await sock.send("Please attach to an organization first".encode("utf8"))
                        else:    
                            org = organization_and_user_list.getOrganization(organization_id)
                            print(org.getOrganizationInfo())
                            #Check if user has permission to delete room TODO: check if the user is owner of the organization
                            #pdb.set_trace()
                            print(request["room_id"])
                            room_id = uuid.UUID(request["room_id"])
                            room = org.getRoom(room_id)
                            if "DELETE" in room.getUserPermissions(client_user_id):
                                #deleting events in room
                                for eventId,_,_ in org.getEventsReservedRoom(room_id):
                                    org.deleteEvent(eventId)
                                #deleting the room    
                                org.deleteRoom(room_id)
                                await sock.send(str.encode("Room deleted"))
                            else:
                                await sock.send("You don't have access for deleting the room".encode("utf8"))    
                    else:
                        await sock.send("Not authorized, please login".encode("utf8"))

            elif request_type == "LIST_RESERVED_EVENTS": #List reserved events in given room
                with mutex:
                    if client_user_id is not None:
                        organization_id = organization_and_user_list.getUser(client_user_id).get_attachedOrganization()
                        if organization_id is None:
                            await sock.send("Please attach to an organization first".encode("utf8"))
                        else:    
                            result = []
                            org = organization_and_user_list.getOrganization(organization_id)
                            #Check if user has permission to list reserved events
                            room_id = uuid.UUID(request["room_id"])
                            room = org.getRoom(room_id)
                            if "LIST" in room.getUserPermissions(client_user_id):
                                for eventId,start,end in org.getEventsReservedRoom(room_id):
                                    result.append({
                                        "event_id": str(eventId),
                                        "event_title": org.getEvent(eventId).getTitle(),
                                        "event_description": org.getEvent(eventId).getDescription(),
                                        "event_category": org.getEvent(eventId).getCategory(),
                                        "event_capacity": str(org.getEvent(eventId).getCapacity()),
                                        "event_duration": str(org.getEvent(eventId).getDuration()),
                                        "event_weekly": str(org.getEvent(eventId).getWeekly()),
                                        "event_hours": str(start) + " - " + str(end),
                                    })
                                    
                                await sock.send(str.encode(json.dumps(result)))
                            else:
                                await sock.send("You don't have access for listing the reserved events".encode("utf8"))    
                    else:
                        await sock.send("Not authorized, please login".encode("utf8"))

            elif request_type == "RESERVE": #Reserve room with given event
                with mutex:
                    if client_user_id is not None:
                        organization_id = organization_and_user_list.getUser(client_user_id).get_attachedOrganization()
                        if organization_id is None:
                            await sock.send("Please attach to an organization first".encode("utf8"))
                        else:    
                            #pdb.set_trace()
                            org = organization_and_user_list.getOrganization(organization_id)
                            room_id = uuid.UUID(request["room_id"])
                            room = org.getRoom(room_id)
                            #Creating event TODO: convert weekly to datetime, right now it is None
                            permissions = { client_user_id :request["event_permissions"]}
                            event = Event(request["event_title"],request["event_description"],request["event_category"],int(request["event_capacity"]),int(request["event_duration"]),None,permissions)
                            org.addEvent(event)
                            #Check if user has permission to reserve room TODO:check for PERRESERVE permission
                            if "RESERVE" in room.getUserPermissions(client_user_id):
                                start = datetime.strptime(request["event_start"], '%Y-%m-%d-%H:%M')
                                org.reserve(event,room,start)
                                await sock.send(str.encode("Room reserved"))
                            else:
                                await sock.send("You don't have access for reserving the room".encode("utf8"))    
                    else:
                        await sock.send("Not authorized, please login".encode("utf8"))

            elif request_type == "DELETE_RESERVATION": #Delete reservation in given room
                with mutex:
                    if client_user_id is not None:
                        organization_id = organization_and_user_list.getUser(client_user_id).get_attachedOrganization()
                        if organization_id is None:
                            await sock.send("Please attach to an organization first".encode("utf8"))
                        else:    
                            org = organization_and_user_list.getOrganization(organization_id)
                            room_id = uuid.UUID(request["room_id"])
                            event_id = uuid.UUID(request["event_id"])
                            room = org.getRoom(room_id)
                            event = org.getEvent(event_id)
                            #Check if user has permission to delete reservation and write to event TODO: check for org owner
                            if "DELETE" in room.getUserPermissions(client_user_id) and "WRITE" in event.getUserPermissions(client_user_id):
                                roomEventList = org.getEventsReservedRoom(room_id)
                                start = datetime.strptime(request["event_start"], '%Y-%m-%d-%H:%M')
                                end = datetime.strptime(request["event_end"], '%Y-%m-%d-%H:%M')
                                roomEventList.remove((event_id,start,end))
                                org.updateRoomReservedByEvent(event_id,None)
                                await sock.send(str.encode("Reservation deleted"))
                            else:
                                await sock.send("You don't have access for deleting the reservation".encode("utf8"))    
                    else:
                        await sock.send("Not authorized, please login".encode("utf8"))
            #Event operations
            elif request_type == "READ_EVENT":
                with mutex:
                    if client_user_id is not None:
                        organization_id = organization_and_user_list.getUser(client_user_id).get_attachedOrganization()
                        if organization_id is None:
                            await sock.send("Please attach to an organization first".encode("utf8"))
                        else:    
                            org = organization_and_user_list.getOrganization(organization_id)
                            event_id = uuid.UUID(request["event_id"])
                            event = org.getEvent(event_id)
                            eventRoomId = org.getRoomReservedByEvent(event_id)
                            if eventRoomId is not None:
                                eventRoom = org.getRoom(eventRoomId)
                            #Check if event is reserved
                            if eventRoomId is None:
                                #Check if user has permission to read event
                                if "READ" in event.getUserPermissions(client_user_id):
                                    await sock.send(f"Event name: {event.getTitle()}, Event Description: {event.getDescription()}, Event Category: {event.getCategory()}, Event Capacity: {event.getCapacity()}\n".encode())
                                else:
                                    await sock.send("You don't have access for reading the event".encode("utf8"))
                            else:
                                #Check if user has permission to read event
                                if "READ" in event.getUserPermissions(client_user_id):
                                    await sock.send(f"Event name: {event.getTitle()}, Event Description: {event.getDescription()}, Event Category: {event.getCategory()}, Event Capacity: {event.getCapacity()}\n".encode())
                                else:
                                    await sock.send(f"{eventRoom.getName()} is busy".encode("utf8"))                     
                    else:
                        await sock.send("Not authorized, please login".encode("utf8"))

            elif request_type == "UPDATE_EVENT":
                with mutex:
                    if client_user_id is not None:
                        organization_id = organization_and_user_list.getUser(client_user_id).get_attachedOrganization()

                        if organization_id is None:
                            await sock.send("Please attach to an organization first".encode("utf8"))
                        else:    
                            org = organization_and_user_list.getOrganization(organization_id)
                            event_id = uuid.UUID(request["event_id"])
                            event = org.getEvent(event_id)
                            #Check if user has permission to update event
                            if "WRITE" in event.getUserPermissions(client_user_id):
                                weekly = None
                                permissions = {}
                                if request["weekly"] != "None":
                                    weekly = datetime.strptime(request["weekly"], '%Y-%m-%d-%H:%M')    
                                org.updateEvent(event_id,request["title"],request["description"],request["category"],int(request["capacity"]),int(request["duration"]),weekly,permissions)
                                await sock.send(str.encode("Event updated"))
                            else:
                                await sock.send("You don't have access for updating the event".encode("utf8"))    
                    else:
                        await sock.send("Not authorized, please login".encode("utf8"))
            elif request_type == "DELETE_EVENT":
                with mutex:
                    if client_user_id is not None:
                        organization_id = organization_and_user_list.getUser(client_user_id).get_attachedOrganization()

                        if organization_id is None:
                            await sock.send("Please attach to an organization first".encode("utf8"))
                        else:    
                            org = organization_and_user_list.getOrganization(organization_id)
                            event_id = uuid.UUID(request["event_id"])
                            event = org.getEvent(event_id)
                            eventRoomId = org.getRoomReservedByEvent(event_id)
                            
                            if eventRoomId is None:
                                if "WRITE" in event.getUserPermissions(client_user_id):
                                    org.deleteEvent(event_id)
                                    await sock.send(str.encode("Event deleted"))    
                                else:
                                    await sock.send("You don't have access for deleting the event".encode("utf8"))
                            else:
                                eventRoom = org.getRoom(eventRoomId)
                                if "WRITE" in event.getUserPermissions(client_user_id) and "DELETE" in eventRoom.getUserPermissions(client_user_id):
                                    org.deleteEvent(event_id)
                                    await sock.send(str.encode("Event deleted"))
                                else:
                                    await sock.send("You don't have access for deleting the event".encode("utf8"))        
                    else:
                        await sock.send("Not authorized, please login".encode("utf8"))                        
            elif request_type == "LOGOUT": #Logout
                with mutex:
                    if client_user_id is not None:
                        #DETACH ORGANIZATION
                        user = organization_and_user_list.getUser(client_user_id)
                        user.update_attachedOrganization(None)
                        #LOGOUT
                        client_user_id = None
                        await sock.send("Logout successful".encode("utf8"))
                    else:    
                        await sock.send("Not authorized, please login".encode("utf8")) 
            elif request_type ==  "SAVE":
                notexit = False
                pickle.dump(organization_and_user_list,open("organizations.p","wb"))
                await sock.send("Exit successful".encode("utf8"))

            pickle.dump(organization_and_user_list,open("organizations.p","wb"))
            received_msg = sock.recv(1024)
        
            
            
    except ConnectionClosedOK:
        print('client is terminating')
    except ConnectionClosedError:
        print('client generated error')

if __name__ == "__main__":
    start_server = websockets.serve(RequestAgent, HOST, PORT)
    asyncio.get_event_loop().run_until_complete(start_server)
    print("WebSocket server is running. Press Ctrl+C to stop.")
    asyncio.get_event_loop().run_forever()
    