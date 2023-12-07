from threading import Thread, Lock, Condition
import socket
import sys
import sqlite3
import json
from json import JSONDecodeError
from .database import Database
from .user import User
import hashlib

import pdb


class Server:
    mutex = Lock()

    def __init__(self, port):
        self.port = port
        self.connected_clients = 0
        sql_db = sqlite3.connect("database.db", check_same_thread=False)
        self.db = Database(sql_db, sql_db.cursor())

    def start_server(self):
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.sock.bind(("", self.port))
        self.sock.listen()

        while True:
            conn, addr = self.sock.accept()

            print("new client", addr)

            RequestHandler(conn, addr, self.db).start()


class RequestHandler(Thread):
    def __init__(self, conn, addr, db):
        self.conn = conn
        self.claddr = addr
        self.current = 0
        self.db = db
        Thread.__init__(self)

    def run(self):
        client_user_id = -1
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

                    user_id = str(user.get_id())
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
            elif request_type == "LOGIN":
                with Server.mutex:
                    username = request["username"]
                    password = request["password"]
                    c = self.db.curs
                    row = c.execute(
                        f"SELECT user_id, password FROM Users WHERE username = '{username}'"
                    ).fetchone()

                    if password == row[1]:
                        print("Login successful")
                    else:
                        print("Login failed")

            received_msg = self.conn.recv(1024)
