import json
from threading import Thread
import socket
import pdb


class Client:
    request_port = 1422
    notification_port = 1428
    address = "localhost"

    def __init__(self):
        self.server_shut_down = False
        self.request_sock = None
        self.notification_sock = None

    def connect(self):
        # Connection to request server port
        self.request_sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.request_sock.connect((self.address, self.request_port))
        # Connection to request server port
        # self.notification_sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        # self.notification_sock.connect((self.address, self.notification_port))

    def make_request(self, request):
        # need to send request in json format
        # pdb.set_trace()
        request_type = request["command"].upper()
        if not self.server_shut_down:
            if request_type == "CREATE_USER":
                self.request_sock.send(str.encode(json.dumps(request)))
                username = self.request_sock.recv(1024).decode("utf8")
                if (
                    username
                ):  # Server returned id of created user which means user creation is successful.
                    print(f"User({username}) created successfully.")

            elif request_type == "LOGIN":
                self.request_sock.send(str.encode(json.dumps(request)))
                return self.request_sock.recv(4096).decode("utf8")

            elif request_type == "LIST_ORGANIZATIONS":
                self.request_sock.send(str.encode(json.dumps(request)))
                return self.request_sock.recv(4096).decode("utf8")

            elif request_type == "ATTACH_ORGANIZATION":
                self.request_sock.send(str.encode(json.dumps(request)))
                return self.request_sock.recv(4096).decode("utf8")

            elif request_type == "DETACH_ORGANIZATION":
                self.request_sock.send(str.encode(json.dumps(request)))
                return self.request_sock.recv(4096).decode("utf8")

            elif request_type == "LIST_ROOMS":  # List rooms in attached organization
                self.request_sock.send(str.encode(json.dumps(request)))
                return self.request_sock.recv(4096).decode("utf8")

            elif request_type == "ADD_ROOM":  # Working hours are in format: %H:%M-%H:%M
                self.request_sock.send(str.encode(json.dumps(request)))
                return self.request_sock.recv(4096).decode("utf8")

            elif request_type == "ACCESS":
                self.request_sock.send(str.encode(json.dumps(request)))
                return self.request_sock.recv(4096).decode("utf8")

            elif request_type == "DELETE_ROOM":
                self.request_sock.send(str.encode(json.dumps(request)))
                return self.request_sock.recv(1024).decode("utf8")

            elif request_type == "LIST_RESERVED_EVENTS":
                self.request_sock.send(str.encode(json.dumps(request)))
                return self.request_sock.recv(4096).decode("utf8")

            elif request_type == "RESERVE":  # Start format is: %Y-%m-%d-%H:%M
                self.request_sock.send(str.encode(json.dumps(request)))
                return self.request_sock.recv(1024).decode("utf8")

            elif (
                request_type == "DELETE_RESERVATION"
            ):  # Start and end are in format: %Y-%m-%d-%H:%M
                self.request_sock.send(str.encode(json.dumps(request)))
                return self.request_sock.recv(1024).decode("utf8")
            elif request_type == "READ_EVENT":
                self.request_sock.send(str.encode(json.dumps(request)))
                return self.request_sock.recv(4096).decode("utf8")
            elif request_type == "UPDATE_EVENT":
                self.request_sock.send(str.encode(json.dumps(request)))
                return self.request_sock.recv(1024).decode("utf8")
            elif request_type == "DELETE_EVENT":
                self.request_sock.send(str.encode(json.dumps(request)))
                return self.request_sock.recv(1024).decode("utf8")
            elif request_type == "QUERY":
                self.request_sock.send(str.encode(json.dumps(request)))
                return self.request_sock.recv(4096).decode("utf8")

            elif request_type == "DAY_VIEW":
                self.request_sock.send(str.encode(json.dumps(request)))
                return self.request_sock.recv(4096).decode("utf8")
            elif request_type == "ROOM_VIEW":
                self.request_sock.send(str.encode(json.dumps(request)))
                return self.request_sock.recv(4096).decode("utf8")
            elif request_type == "LOGOUT":
                self.request_sock.send(str.encode(json.dumps(request)))
                return self.request_sock.recv(1024).decode("utf8")

            elif request_type == "EXIT":
                self.request_sock.send(str.encode(json.dumps(request)))
                return self.request_sock.recv(1024).decode("utf8")
                self.server_shut_down = True
            elif request_type == "SAVE":
                self.request_sock.send(str.encode(json.dumps(request)))
                return self.request_sock.recv(1024).decode("utf8")

            else:
                return "Invalid command"

        def notification(self, user_id):
            pass
            # while not self.server_shut_down:
            #     try:
            #         notification = self.notification_sock.recv(1024).decode("utf8")
            #         notification = json.loads(notification)
            #         if notification["user_id"] == user_id:
            #             print(notification["message"])
            #     except json.JSONDecodeError:
            #         print("Invalid notification format")
            #     except ConnectionResetError:
            #         print("Server is shut down")
            #         self.server_shut_down = True
            #         break


if __name__ == "__main__":
    client = Client()
    client.connect()
