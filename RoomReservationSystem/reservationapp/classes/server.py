from threading import Thread, Lock, Condition
import socket
import sys
import sqlite3
import json
from json import JSONDecodeError
from database import Database
from room import Room
from user import User
import hashlib
import pickle
import pdb
from datetime import datetime
from singletonCatalgoue import Catalogue
import uuid


class Server:
    mutex = Lock()
    organization_and_user_list= Catalogue()
    userList = {}
    def __init__(self, request_port,notification_port):
        self.request_port = request_port
        self.notification_port = notification_port
        self.connected_clients = 0
        sql_db = sqlite3.connect("database.db", check_same_thread=False)
        try:
            self.organization_and_user_list = pickle.load(open("organizations.p","rb"))
            print(self.organization_and_user_list.getOrganizationList().keys())
            print(self.organization_and_user_list.getUserList().keys())
        except FileNotFoundError as err:
            print("error:" + str(err))
               
        self.db = Database(sql_db, sql_db.cursor())
        

    def __del__(self):
        pickle.dump(self.organization_and_user_list,open("organizations.p","wb"))
        print("Server shutdown, file saved")

    def start_request_server(self):
        #For requests
        self.request_sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.request_sock.bind(("", self.request_port))
        self.request_sock.listen()

        while True:
            conn, addr = self.request_sock.accept()
            print("new client")
            RequestHandler(conn,addr, self.db).start()

    def start_notification_server(self):
        #For notifications
        self.notifcation_sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.notifcation_sock.bind(("", self.notification_port))
        self.notifcation_sock.listen()

        while True:
            conn, addr = self.notifcation_sock.accept()
            NotificationHandler(conn,addr, self.db).start()

    def start_server(self):
        request_server = Thread(target=self.start_request_server)
        request_server.start()
        notification_server = Thread(target=self.start_notification_server)
        notification_server.start()      



class RequestHandler(Thread):
    def __init__(self, conn,addr, db):
        self.conn = conn
        self.addr = addr
        self.current = 0
        self.db = db
        Thread.__init__(self)

    def run(self):
        print("Request server started")
        client_user_id = None
        notexit = True
        received_msg = self.conn.recv(1024)
        while notexit and received_msg != b"":
            decode8 = received_msg.decode("utf8")
            try:
                request = json.loads(decode8)
            except JSONDecodeError:
                notexit = False

            request_type = request["command"]
            request["user_id"] = client_user_id

            if request_type == "CREATE_USER":  # CREATE_USER
                with Server.mutex:
                   

                    user = User(
                        request["username"],
                        request["email"],
                        request["fullname"],
                        request["password"],
                    )
                    
                    user_id = str(user.getId())
                    django_id = request["django_id"]

                    #Add user to catalogue
                    Server.organization_and_user_list.addUser(user)

                    self.db.insert(
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
                    self.conn.send(str.encode(user.get_fullname()))

            elif request_type == "LOGIN": #LOGIN
                with Server.mutex:
                    print(request)
                    username = request["username"]
                    encoded_password = request["password"]

                    c = self.db.curs
                    
                    row = c.execute(
                        f"SELECT user_id, password FROM Users WHERE username = '{username}'"
                    ).fetchone()

                    if encoded_password == row[1]:
                        print("Login successful")
                        client_user_id = uuid.UUID(row[0])
                        #print(client_user_id)
                        self.conn.send("Login successful".encode("utf8"))
                    else:
                        print("Login failed")
                        self.conn.send("Login failed".encode("utf8"))


            #Organization operations
            elif request_type ==  "LIST_ORGANIZATIONS": #List organizations
                with Server.mutex:
                    result = []
                    if client_user_id is not None:
                        for organization in Server.organization_and_user_list.getOrganizationList().values():
                            result.append(organization.getOrganizationInfo())
                        self.conn.send(str.encode(json.dumps(result)))
                    else:
                        self.conn.send("Not authorized, please login".encode("utf8"))    
            
            elif request_type == "ATTACH_ORGANIZATION": #Attaching organization to user
                with Server.mutex:
                    if client_user_id is not None:
                        organization_id = uuid.UUID(request["organization_id"])
                        user = Server.organization_and_user_list.getUser(client_user_id)
                        user.update_attachedOrganization(organization_id)
                        self.conn.send(str.encode("Organization attached"))
                    else:
                        self.conn.send("Not authorized, please login".encode("utf8"))

            elif request_type == "DETACH_ORGANIZATION": #Attaching organization to user
                with Server.mutex:
                    if client_user_id is not None:
                        user = Server.organization_and_user_list.getUser(client_user_id)
                        user.update_attachedOrganization(None)
                        self.conn.send(str.encode("Organization detached"))
                    else:
                        self.conn.send("Not authorized, please login".encode("utf8"))            

            elif request_type == "LIST_ROOMS": #Listing rooms
                with Server.mutex:
                    if client_user_id is not None:
                        organization_id = Server.organization_and_user_list.getUser(client_user_id).get_attachedOrganization()
                        if organization_id is None:
                            self.conn.send("Please attach to an organization first".encode("utf8"))
                        else:    
                            org = Server.organization_and_user_list.getOrganization(organization_id)
                            #Check if user has permission to list rooms
                           
                            if "LIST" in org.getUserPermissions(client_user_id):
                                self.conn.send(str.encode(json.dumps(org.listRooms())))
                            else:
                                self.conn.send("You don't have access for listing the rooms".encode("utf8"))    
                    else:
                        self.conn.send("Not authorized, please login".encode("utf8"))

            elif request_type == "ADD_ROOM": #Adding room
                with Server.mutex:
                    if client_user_id is not None:
                        organization_id = Server.organization_and_user_list.getUser(client_user_id).get_attachedOrganization()
                        if organization_id is None:
                            self.conn.send("Please attach to an organization first".encode("utf8"))
                        else:    
                            org = Server.organization_and_user_list.getOrganization(organization_id)
                            #Check if user has permission to add rooms
                            if "ADD" in org.getUserPermissions(client_user_id):
                                start_end = request["working_hours"].split("-")
                                start = datetime.strptime(start_end[0], "%H:%M").time()
                                end = datetime.strptime(start_end[1], "%H:%M").time()
                                working_hours = (start,end)
                                #Room with no permissions
                                permissions = {}
                                room = Room(request["room_name"],int(request["x"]),int(request["y"]),int(request["capacity"]),working_hours,permissions)
                                org.addRoom(room)
                                self.conn.send(str.encode("Room added"))
                            else:
                                self.conn.send("You don't have access for adding rooms".encode("utf8"))    
                    else:
                        self.conn.send("Not authorized, please login".encode("utf8"))

            elif request_type == "ACCESS": #Accessing rooms and events
                with Server.mutex:
                    if client_user_id is not None:
                        organization_id = Server.organization_and_user_list.getUser(client_user_id).get_attachedOrganization()
                        if organization_id is None:
                            self.conn.send("Please attach to an organization first".encode("utf8"))
                        else:    
                            org = Server.organization_and_user_list.getOrganization(organization_id)
                            if "ACCESS" in org.getUserPermissions(client_user_id):
                                self.conn.sendall(str.encode(org.accessRoomsandEvents()))
                            else:
                                self.conn.send("You don't have access for accessing rooms and events".encode("utf8"))
                    else:
                        self.conn.send("Not authorized, please login".encode("utf8"))

            #Room operations
            elif request_type == "DELETE_ROOM": #Deleting room
                with Server.mutex:
                    if client_user_id is not None:
                        organization_id = Server.organization_and_user_list.getUser(client_user_id).get_attachedOrganization()
                        if organization_id is None:
                            self.conn.send("Please attach to an organization first".encode("utf8"))
                        else:    
                            org = Server.organization_and_user_list.getOrganization(organization_id)
                            #Check if user has permission to delete room TODO: check if the user is owner of the organization
                            room_id = uuid.UUID(request["room_id"])
                            room = org.getRoom(room_id)
                            if "DELETE" in room.getUserPermissions(client_user_id):
                                #deleting events in room
                                for eventId,_,_ in org.getEventsReservedRoom(room_id):
                                    org.deleteEvent(eventId)
                                #deleting the room    
                                org.deleteRoom(room_id)
                                self.conn.send(str.encode("Room deleted"))
                            else:
                                self.conn.send("You don't have access for deleting the room".encode("utf8"))    
                    else:
                        self.conn.send("Not authorized, please login".encode("utf8"))

            elif request_type == "LIST_RESERVED_EVENTS": #List reserved events in given room
                with Server.mutex:
                    if client_user_id is not None:
                        organization_id = Server.organization_and_user_list.getUser(client_user_id).get_attachedOrganization()
                        if organization_id is None:
                            self.conn.send("Please attach to an organization first".encode("utf8"))
                        else:    
                            result = ""
                            org = Server.organization_and_user_list.getOrganization(organization_id)
                            #Check if user has permission to list reserved events
                            room_id = uuid.UUID(request["room_id"])
                            room = org.getRoom(room_id)
                            if "LIST" in room.getUserPermissions(client_user_id):
                                for eventId,start,end in org.getEventsReservedRoom(room_id):
                                    result += f"Event name: {org.getEvent(eventId).getTitle()} Start: {start} End: {end}\n"
                                if result == "":
                                    self.conn.send("No events reserved".encode("utf8"))
                                else:        
                                    self.conn.send(str.encode(result))
                            else:
                                self.conn.send("You don't have access for listing the reserved events".encode("utf8"))    
                    else:
                        self.conn.send("Not authorized, please login".encode("utf8"))

            elif request_type == "RESERVE": #Reserve room with given event
                with Server.mutex:
                    if client_user_id is not None:
                        organization_id = Server.organization_and_user_list.getUser(client_user_id).get_attachedOrganization()
                        if organization_id is None:
                            self.conn.send("Please attach to an organization first".encode("utf8"))
                        else:    
                            org = Server.organization_and_user_list.getOrganization(organization_id)
                            room_id = uuid.UUID(request["room_id"])
                            room = org.getRoom(room_id)
                            #Check if user has permission to reserve room TODO:check for PERRESERVE permission
                            if "RESERVE" in room.getUserPermissions(client_user_id):
                                event_id = uuid.UUID(request["event_id"])
                                start = datetime.strptime(request["start"], '%Y-%m-%d-%H:%M')
                                org.reserve(org.getEvent(event_id),room,start)
                                self.conn.send(str.encode("Room reserved"))
                            else:
                                self.conn.send("You don't have access for reserving the room".encode("utf8"))    
                    else:
                        self.conn.send("Not authorized, please login".encode("utf8"))

            elif request_type == "DELETE_RESERVATION": #Delete reservation in given room
                with Server.mutex:
                    if client_user_id is not None:
                        organization_id = Server.organization_and_user_list.getUser(client_user_id).get_attachedOrganization()
                        if organization_id is None:
                            self.conn.send("Please attach to an organization first".encode("utf8"))
                        else:    
                            org = Server.organization_and_user_list.getOrganization(organization_id)
                            room_id = uuid.UUID(request["room_id"])
                            event_id = uuid.UUID(request["event_id"])
                            room = org.getRoom(room_id)
                            event = org.getEvent(event_id)
                            #Check if user has permission to delete reservation and write to event TODO: check for org owner
                            if "DELETE" in room.getUserPermissions(client_user_id) and "WRITE" in event.getUserPermissions(client_user_id):
                                roomEventList = org.getEventsReservedRoom(room_id)
                                start = datetime.strptime(request["start"], '%Y-%m-%d-%H:%M')
                                end = datetime.strptime(request["end"], '%Y-%m-%d-%H:%M')
                                roomEventList.remove((event_id,start,end))
                                org.updateRoomReservedByEvent(event_id,None)
                                self.conn.send(str.encode("Reservation deleted"))
                            else:
                                self.conn.send("You don't have access for deleting the reservation".encode("utf8"))    
                    else:
                        self.conn.send("Not authorized, please login".encode("utf8"))
            #Event operations
            elif request_type == "READ_EVENT":
                with Server.mutex:
                    if client_user_id is not None:
                        organization_id = Server.organization_and_user_list.getUser(client_user_id).get_attachedOrganization()
                        if organization_id is None:
                            self.conn.send("Please attach to an organization first".encode("utf8"))
                        else:    
                            org = Server.organization_and_user_list.getOrganization(organization_id)
                            event_id = uuid.UUID(request["event_id"])
                            event = org.getEvent(event_id)
                            eventRoomId = org.getRoomReservedByEvent(event_id)
                            if eventRoomId is not None:
                                eventRoom = org.getRoom(eventRoomId)
                            #Check if event is reserved
                            if eventRoomId is None:
                                #Check if user has permission to read event
                                if "READ" in event.getUserPermissions(client_user_id):
                                    self.conn.send(f"Event name: {event.getTitle()}, Event Description: {event.getDescription()}, Event Category: {event.getCategory()}, Event Capacity: {event.getCapacity()}\n".encode())
                                else:
                                    self.conn.send("You don't have access for reading the event".encode("utf8"))
                            else:
                                #Check if user has permission to read event
                                if "READ" in event.getUserPermissions(client_user_id):
                                    self.conn.send(f"Event name: {event.getTitle()}, Event Description: {event.getDescription()}, Event Category: {event.getCategory()}, Event Capacity: {event.getCapacity()}\n".encode())
                                else:
                                    self.conn.send(f"{eventRoom.getName()} is busy".encode("utf8"))                     
                    else:
                        self.conn.send("Not authorized, please login".encode("utf8"))

            elif request_type == "UPDATE_EVENT":
                with Server.mutex:
                    if client_user_id is not None:
                        organization_id = Server.organization_and_user_list.getUser(client_user_id).get_attachedOrganization()

                        if organization_id is None:
                            self.conn.send("Please attach to an organization first".encode("utf8"))
                        else:    
                            org = Server.organization_and_user_list.getOrganization(organization_id)
                            event_id = uuid.UUID(request["event_id"])
                            event = org.getEvent(event_id)
                            #Check if user has permission to update event
                            if "WRITE" in event.getUserPermissions(client_user_id):
                                weekly = None
                                permissions = {}
                                if request["weekly"] != "None":
                                    weekly = datetime.strptime(request["weekly"], '%Y-%m-%d-%H:%M')    
                                org.updateEvent(event_id,request["title"],request["description"],request["category"],int(request["capacity"]),int(request["duration"]),weekly,permissions)
                                self.conn.send(str.encode("Event updated"))
                            else:
                                self.conn.send("You don't have access for updating the event".encode("utf8"))    
                    else:
                        self.conn.send("Not authorized, please login".encode("utf8"))
            elif request_type == "DELETE_EVENT":
                with Server.mutex:
                    if client_user_id is not None:
                        organization_id = Server.organization_and_user_list.getUser(client_user_id).get_attachedOrganization()

                        if organization_id is None:
                            self.conn.send("Please attach to an organization first".encode("utf8"))
                        else:    
                            org = Server.organization_and_user_list.getOrganization(organization_id)
                            event_id = uuid.UUID(request["event_id"])
                            event = org.getEvent(event_id)
                            eventRoomId = org.getRoomReservedByEvent(event_id)
                            
                            if eventRoomId is None:
                                if "WRITE" in event.getUserPermissions(client_user_id):
                                    org.deleteEvent(event_id)
                                    self.conn.send(str.encode("Event deleted"))    
                                else:
                                    self.conn.send("You don't have access for deleting the event".encode("utf8"))
                            else:
                                eventRoom = org.getRoom(eventRoomId)
                                if "WRITE" in event.getUserPermissions(client_user_id) and "DELETE" in eventRoom.getUserPermissions(client_user_id):
                                    org.deleteEvent(event_id)
                                    self.conn.send(str.encode("Event deleted"))
                                else:
                                    self.conn.send("You don't have access for deleting the event".encode("utf8"))        
                    else:
                        self.conn.send("Not authorized, please login".encode("utf8"))                        
            elif request_type == "LOGOUT": #Logout
                with Server.mutex:
                    if client_user_id is not None:
                        #DETACH ORGANIZATION
                        user = Server.organization_and_user_list.getUser(client_user_id)
                        user.update_attachedOrganization(None)
                        #LOGOUT
                        client_user_id = None
                        self.conn.send("Logout successful".encode("utf8"))
                    else:    
                        self.conn.send("Not authorized, please login".encode("utf8")) 
            elif request_type ==  "SAVE":
                notexit = False
                pickle.dump(Server.organization_and_user_list,open("organizations.p","wb"))
                self.conn.send("Exit successful".encode("utf8"))


            received_msg = self.conn.recv(1024)
              
        #Kill connection    
        self.conn.close()
class NotificationHandler(Thread):
    def __init__(self, conn,addr, db):
        self.conn = conn
        self.addr = addr
        self.current = 0
        self.db = db
        Thread.__init__(self)

    def run(self):
        #For notifications
        print("Notification server started")
        client_user_id = None
        notexit = True
        received_msg = self.conn.recv(1024)
        while notexit and received_msg != b"":
            decode8 = received_msg.decode("utf8")
            try:
                request = json.loads(decode8)
            except JSONDecodeError:
                notexit = False

            request_type = request["command"]
            request["user_id"] = client_user_id

            if request_type ==  "EXIT":
                notexit = False
                self.conn.send("Exit successful".encode("utf8"))

            received_msg = self.conn.recv(1024)
              
        #Kill connection    
        self.conn.close()     

if __name__ == "__main__":
    
    server = Server(1422,1428)

    server.start_server()

  
