import json
from threading import Thread
import socket


class Client:
    port = 1423
    address = "localhost"

    def __init__(self):
        self.server_shut_down = False
        self.sock = None

    def connect(self):
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.sock.connect((self.address, self.port))

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

            if request_type == "CREATE_USER" or request_type == "0":
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

                self.sock.send(str.encode(json.dumps(request)))
                username = self.sock.recv(1024).decode("utf8")
                if (
                    username
                ):  # Server returned id of created user which means user creation is successful.
                    print(f"User({username}) created successfully.")

            elif request_type == "LOGIN" or request_type == "1":
                if not is_json:
                    params = request.split(" ")
                    username = params[1]
                    password = params[2]
                    request = {
                        "command": "LOGIN",
                        "username": username,
                        "password": password,
                    }

                self.sock.send(str.encode(json.dumps(request)))
                user_id = int(self.sock.recv(1024).decode("utf8"))
                if (
                    user_id >= 0
                ):  # Server returned id of logged in user which means user login is successful.
                    self.logged_in_user_id = user_id
                    print(f"User({request['username']}) is logged in.")
                    notification_thread = Thread(
                        target=self.notification, args=(user_id,)
                    )  # msh[0] is user_id
                    notification_thread.start()


if __name__ == "__main__":
    client = Client()
    client.connect()
