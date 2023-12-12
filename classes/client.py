import json
from threading import Thread
import socket


class Client:
    request_port = 1422
    notifiaction_port = 1428
    address = "localhost"

    def __init__(self):
        self.server_shut_down = False
        self.request_sock = None
        self.notification_sock = None

    def connect(self):

        #Connection to request server port
        self.request_sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.request_sock.connect((self.address, self.request_port))
        #Connection to request server port
        self.notification_sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.notification_sock.connect((self.address, self.notifiaction_port))

        while not self.server_shut_down:
            is_json = False

            request = input("\nRequest: ")
            try:
                request = json.loads(request)
                if type(request) == int:
                    request_type = request
                else:
                    request_type = request["command"]
                is_json = True
            except json.JSONDecodeError:
                request_type = request.split(" ")[0]

            if request_type == "CREATE_USER":
                if not is_json:
                    params = request.split(" ")
                    username = params[1]
                    email = params[2]
                    fullname = params[3]
                    password = params[4]

                    request = {
                        "command": "CREATE_USER",
                        "username": username,
                        "email": email,
                        "fullname": fullname,
                        "password": password,
                    }

                self.request_sock.send(str.encode(json.dumps(request)))
                username = self.request_sock.recv(1024).decode("utf8")
                if (
                    username
                ):  # Server returned id of created user which means user creation is successful.
                    print(f"User({username}) created successfully.")

            elif request_type == "LOGIN":
                if not is_json:
                    params = request.split(" ")
                    username = params[1]
                    password = params[2]
                    request = {
                        "command": "LOGIN",
                        "username": username,
                        "password": password,
                    }

                self.request_sock.send(str.encode(json.dumps(request)))
                print(self.request_sock.recv(1024).decode("utf8"))
                # if (
                #     user_id >= 0
                # ):  # Server returned id of logged in user which means user login is successful.
                #     self.logged_in_user_id = user_id
                #     print(f"User({request['username']}) is logged in.")
                #     notification_thread = Thread(
                #         target=self.notification, args=(user_id,)
                #     )  # msh[0] is user_id
                #     notification_thread.start()
            elif request_type == "LIST_OBJECT":
                if not is_json:
                    params = request.split(" ")
                    request = {
                        "command": "LIST_OBJECT",
                    }
                self.request_sock.send(str.encode(json.dumps(request)))
                print(self.request_sock.recv(1024).decode("utf8"))

            elif request_type == "ATTACH_ORGANIZATION":
                if not is_json:
                    params = request.split(" ")
                    request = {
                        "command": "ATTACH_ORGANIZATION",
                        "organization_id": params[1],
                    }
                self.request_sock.send(str.encode(json.dumps(request)))
                print(self.request_sock.recv(1024).decode("utf8"))

            elif request_type == "LIST_ROOM": #List rooms in attached organization
                if not is_json:
                    params = request.split(" ")
                    request = {
                        "command": "LIST_ROOM",
                    }
                self.request_sock.send(str.encode(json.dumps(request)))
                print(self.request_sock.recv(1024).decode("utf8"))

            elif request_type == "ADD_ROOM":
                if not is_json:
                    params = request.split(" ")
                    request = {
                        "command": "ADD_ROOM",
                        "room_name": params[1],
                        "room_x": params[2],
                        "room_y": params[3],
                        "capacity": params[4],
                        "working_hours": params[5],
                        "permissions": params[6],
                    }
                self.request_sock.send(str.encode(json.dumps(request)))
                print(self.request_sock.recv(1024).decode("utf8"))

            elif request_type == "ACCESS":
                if not is_json:
                    params = request.split(" ")
                    request = {
                        "command": "ACCESS",
                    }
                self.request_sock.send(str.encode(json.dumps(request)))
                print(self.request_sock.recv(1024).decode("utf8"))

            elif request_type == "DELETE_ROOM":
                if not is_json:
                    params = request.split(" ")
                    request = {
                        "command": "DELETE_ROOM",
                        "room_id": params[1],
                    }
                self.request_sock.send(str.encode(json.dumps(request)))
                print(self.request_sock.recv(1024).decode("utf8"))

            elif request_type == "LIST_RESERVED_EVENTS":
                if not is_json:
                    params = request.split(" ")
                    request = {
                        "command": "LIST_RESERVED_EVENTS",
                        "room_id": params[1],
                    }
                self.request_sock.send(str.encode(json.dumps(request)))
                print(self.request_sock.recv(1024).decode("utf8"))

            elif request_type == "RESERVE":
                if not is_json:
                    params = request.split(" ")
                    request = {
                        "command": "RESERVE",
                        "room_id": params[1],
                        "event_id": params[2],
                        "start": params[3],
                        "end": params[4],
                    }
                self.request_sock.send(str.encode(json.dumps(request)))
                print(self.request_sock.recv(1024).decode("utf8"))

            elif request_type == "DELETE_RESERVATION":
                if not is_json:
                    params = request.split(" ")
                    request = {
                        "command": "DELETE_RESERVATIONS",
                        "room_id": params[1],
                        "event_id": params[2],
                    }
                self.request_sock.send(str.encode(json.dumps(request)))
                print(self.request_sock.recv(1024).decode("utf8"))
            elif request_type == "READ_EVENT":
                if not is_json:
                    params = request.split(" ")
                    request = {
                        "command": "READ_EVENT",
                        "event_id": params[1],
                    }
                self.request_sock.send(str.encode(json.dumps(request)))
                print(self.request_sock.recv(1024).decode("utf8"))    
            elif request_type == "UPDATE_EVENT":
                if not is_json:
                    params = request.split(" ")
                    request = {
                        "command": "UPDATE_EVENT",
                        "title": params[1],
                        "description": params[2],
                        "category": params[3],
                        "capacity": params[4],
                        "duration": params[5],
                        "weekly": params[6],
                        "permissions": params[7],
                    }
                self.request_sock.send(str.encode(json.dumps(request)))
                print(self.request_sock.recv(1024).decode("utf8"))
            elif request_type == "DELETE_EVENT":
                if not is_json:
                    params = request.split(" ")
                    request = {
                        "command": "DELETE_EVENT",
                        "event_id": params[1],
                    }
                self.request_sock.send(str.encode(json.dumps(request)))
                print(self.request_sock.recv(1024).decode("utf8"))                   
            elif request_type == "LOGOUT":
                if not is_json:
                    params = request.split(" ")
                    request = {
                        "command": "LOGOUT",
                    }
                self.request_sock.send(str.encode(json.dumps(request)))
                print(self.request_sock.recv(1024).decode("utf8"))

            elif request_type == "EXIT":
                if not is_json:
                    params = request.split(" ")
                    request = {
                        "command": "EXIT",
                    }
                self.request_sock.send(str.encode(json.dumps(request)))
                print(self.request_sock.recv(1024).decode("utf8"))
                self.server_shut_down = True            


if __name__ == "__main__":
    client = Client()
    client.connect()
