import hashlib
import sqlite3
import uuid


class User:
    def __init__(self, username, email, fullname, passwd):
        self.username = username
        self.email = email
        self.fullname = fullname
        self.passwd = passwd
        self.token = None

    def get_username(self):
        return self.username

    def get_email(self):
        return self.email

    def get_fullname(self):
        return self.fullname

    def get_passwd(self):
        return self.passwd

    def auth(self, plainpass):
        return self.passwd == plainpass

    def login(self):
        self.token = uuid.uuid4()
        return self.token

    def checksession(self, token):
        return self.token == token

    def logout(self):
        self.token = None
