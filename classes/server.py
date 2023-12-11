from threading import Thread, Lock, Condition
import socket
import sys
import sqlite3
import json
from json import JSONDecodeError
from .database import Database
from .room import Room
from .user import User
import hashlib
import pickle
import pdb
from .singletonCatalgoue import Catalogue
import uuid


class Server:
    mutex = Lock()
    organization_and_user_list= Catalogue()
    logged_in_users = {}
    def __init__(self, request_port,notification_port):
        self.request_port = request_port
        self.notification_port = notification_port
        self.connected_clients = 0
        sql_db = sqlite3.connect("database.db", check_same_thread=False)
        try:
            self.organization_and_user_list = pickle.load(open("organizations.p","rb"))
            print(self.organization_and_user_list.getOrganizationList().keys())
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
                    encoded_password = hashlib.sha256(request["password"].encode()).hexdigest()

                    user = User(
                        request["username"],
                        request["email"],
                        request["fullname"],
                        encoded_password,
                    )
                    
                    user_id = str(user.getId())

                    #Add user to catalogue
                    Server.organization_and_user_list.addUser(user)

                    self.db.insert(
                        "Users",
                        ("user_id", "username", "email", "fullname", "password"),
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
                    username = request["username"]
                    encoded_password = hashlib.sha256(request["password"].encode()).hexdigest()
                    c = self.db.curs
                    row = c.execute(
                        f"SELECT user_id, password FROM Users WHERE username = '{username}'"
                    ).fetchone()

                    if encoded_password == row[1]:
                        print("Login successful")
                        client_user_id = uuid.UUID(row[0])
                        self.conn.send("Login successful".encode("utf8"))
                    else:
                        print("Login failed")
                        self.conn.send("Login failed".encode("utf8"))

            elif request_type ==  "LIST_OBJECT": #List organizations
                with Server.mutex:
                    result = ""
                    if client_user_id is not None:
                        for organization in Server.organization_and_user_list.getOrganizationList().values():
                            result += organization.getOrganizationInfo()
                        self.conn.send(str.encode(result))
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

            elif request_type == "LIST_ROOM": #Listing rooms
                with Server.mutex:
                    if client_user_id is not None:
                        organization_id = Server.organization_and_user_list.getUser(client_user_id).get_attachedOrganization()
                        if organization_id is None:
                            self.conn.send("Please attach to an organization first".encode("utf8"))
                        else:    
                            org = Server.organization_and_user_list.get(organization_id)
                            self.conn.send(str.encode(org.listRooms()))
                    else:
                        self.conn.send("Not authorized, please login".encode("utf8"))

            elif request_type == "ADD_ROOM": #Adding room
                with Server.mutex:
                    if client_user_id is not None:
                        organization_id = Server.organization_and_user_list.getUser(client_user_id).get_attachedOrganization()
                        if organization_id is None:
                            self.conn.send("Please attach to an organization first".encode("utf8"))
                        else:    
                            org = Server.organization_and_user_list.get(organization_id)
                            room = Room(request["room_name"],request["x"],request["y"],request["capacity"],request["working_hours"],request["permissions"])
                            org.addRoom(room)
                            self.conn.send(str.encode("Room added"))
                    else:
                        self.conn.send("Not authorized, please login".encode("utf8"))

            elif request_type == "ACCESS": #Accessing rooms and events
                with Server.mutex:
                    if client_user_id is not None:
                        organization_id = Server.organization_and_user_list.getUser(client_user_id).get_attachedOrganization()
                        if organization_id is None:
                            self.conn.send("Please attach to an organization first".encode("utf8"))
                        else:    
                            org = Server.organization_and_user_list.get(organization_id)
                            self.conn.send(str.encode(org.accessRoomsandEvents()))
                    else:
                        self.conn.send("Not authorized, please login".encode("utf8"))

            elif request_type == "DELETE_ROOM": #Deleting room
                with Server.mutex:
                    if client_user_id is not None:
                        organization_id = Server.organization_and_user_list.getUser(client_user_id).get_attachedOrganization()
                        if organization_id is None:
                            self.conn.send("Please attach to an organization first".encode("utf8"))
                        else:    
                            org = Server.organization_and_user_list.get(organization_id)
                            #deleting events in room
                            for eventId,_,_ in org.getRoom(request["room_id"])[1]:
                                org.deleteEvent(eventId)
                            #deleting the room    
                            org.deleteRoom(request["room_id"])
                            self.conn.send(str.encode("Room deleted"))
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
                            org = Server.organization_and_user_list.get(organization_id)
                            for eventId,start,end in org.getRoom(request["room_id"])[1]:
                                result += f"Event name: {org.getEvent(eventId)[0].getTitle()} Start: {start} End: {end}\n"
                            self.conn.send(str.encode(result))
                    else:
                        self.conn.send("Not authorized, please login".encode("utf8"))

            elif request_type == "RESERVE": #Reserve room with given event
                with Server.mutex:
                    if client_user_id is not None:
                        organization_id = Server.organization_and_user_list.getUser(client_user_id).get_attachedOrganization()
                        if organization_id is None:
                            self.conn.send("Please attach to an organization first".encode("utf8"))
                        else:    
                            org = Server.organization_and_user_list.get(organization_id)
                            org.reserveRoom(org.getRoom(request["room_id"])[0],org.getEvent(request["event_id"])[0],request["start"],request["end"])
                            self.conn.send(str.encode("Room reserved"))
                    else:
                        self.conn.send("Not authorized, please login".encode("utf8"))

            elif request_type == "DELETE_RESERVATIONS": #Delete reservations in given room
                with Server.mutex:
                    if client_user_id is not None:
                        organization_id = Server.organization_and_user_list.getUser(client_user_id).get_attachedOrganization()
                        if organization_id is None:
                            self.conn.send("Please attach to an organization first".encode("utf8"))
                        else:    
                            org = Server.organization_and_user_list.get(organization_id)
                            for eventId,start,end in org.getRoom(request["room_id"])[1]:
                                org.getEvent(eventId)[1] = None
                                org.getRoom(request["room_id"])[1].remove((eventId,start,end))
                            self.conn.send(str.encode("Reservations deleted"))
                    else:
                        self.conn.send("Not authorized, please login".encode("utf8"))

            elif request_type == "READ_EVENTS":
                with Server.mutex:
                    if client_user_id is not None:
                        organization_id = Server.organization_and_user_list.getUser(client_user_id).get_attachedOrganization()
                        result = ""
                        if organization_id is None:
                            self.conn.send("Please attach to an organization first".encode("utf8"))
                        else:    
                            org = Server.organization_and_user_list.get(organization_id)
                            self.conn.send(str.encode(org.listEvents()))
                    else:
                        self.conn.send("Not authorized, please login".encode("utf8"))
            elif request_type == "UPDATE_EVENT":
                with Server.mutex:
                    if client_user_id is not None:
                        organization_id = Server.organization_and_user_list.getUser(client_user_id).get_attachedOrganization()

                        if organization_id is None:
                            self.conn.send("Please attach to an organization first".encode("utf8"))
                        else:    
                            org = Server.organization_and_user_list.get(organization_id)
                            org.updateEvent(request["title"],request["description"],request["category"],request["capacity"],request["duration"],request["weekly"],request["permissions"])
                            self.conn.send(str.encode("Event updated"))
                    else:
                        self.conn.send("Not authorized, please login".encode("utf8"))
            elif request_type == "DELETE_EVENT":
                with Server.mutex:
                    if client_user_id is not None:
                        organization_id = Server.organization_and_user_list.getUser(client_user_id).get_attachedOrganization()

                        if organization_id is None:
                            self.conn.send("Please attach to an organization first".encode("utf8"))
                        else:    
                            org = Server.organization_and_user_list.get(organization_id)
                            org.deleteEvent(request["event_id"])
                            self.conn.send(str.encode("Event deleted"))
                    else:
                        self.conn.send("Not authorized, please login".encode("utf8"))                        
            elif request_type == "LOGOUT": #Logout
                with Server.mutex:
                    if client_user_id is not None:
                        client_user_id = None
                        self.conn.send("Logout successful".encode("utf8"))
                    else:    
                        self.conn.send("Not authorized, please login".encode("utf8")) 
            elif request_type ==  "EXIT":
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
