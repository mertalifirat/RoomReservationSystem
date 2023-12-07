from classes.server import Server
from classes.view import View
from classes.user import User

server = Server(1423)

user1 = User("admin", "admin@localhost", "Admin", "admin1234")
user2 = User("user", "user@localhost", "User", "user1234")

server.start_server()
