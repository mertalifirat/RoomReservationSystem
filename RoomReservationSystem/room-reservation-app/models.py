from django.db import models

class Singleton(object):
    
    def __new__(cls):
        if not hasattr(cls,'_inst'):
            cls._inst = super(Singleton,cls).__new__(cls)
        return cls._inst
# Create your models here.
class ClientManager(Singleton):

    def __init__(self):
        self.clientList = {} # key: client_id, value: client

    def addClient(self, client):
        self.clientList[client.client_id] = client
    def getClient(self, client_id):
        return self.clientList[client_id]
    def removeClient(self, client_id):
        del self.clientList[client_id]   

             
    
