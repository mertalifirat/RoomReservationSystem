import hashlib
import sqlite3
import uuid


class User:
    def __init__(self, username, email, fullname, passwd):
        self.id = uuid.uuid4()
        self.username = username
        self.email = email
        self.fullname = fullname
        self.passwd = passwd
        self.token = None

    def __del__(self):
        print("User {} deleted".format(self.username))

    def get_id(self):
        return self.id

    def get_username(self):
        return self.username

    def get_email(self):
        return self.email

    def get_fullname(self):
        return self.fullname

    def get_passwd(self):
        return self.passwd

    def get_token(self):
        return self.token

    def update_username(self, username):
        self.username = username

    def update_email(self, email):
        self.email = email

    def update_fullname(self, fullname):
        self.fullname = fullname

    def update_passwd(self, passwd):
        self.passwd = passwd

    def update_token(self, token):
        self.token = token

    def auth(self, plainpass):
        return self.passwd == plainpass

    def login(self):
        self.token = uuid.uuid4()
        return self.token

    def checksession(self, token):
        return self.token == token

    def logout(self):
        self.token = None
