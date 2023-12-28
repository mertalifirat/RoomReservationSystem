from django.db import models

class Singleton(object):
    
    def __new__(cls):
        if not hasattr(cls,'_inst'):
            cls._inst = super(Singleton,cls).__new__(cls)
        return cls._inst
# Create your models here.
class ClientManager(Singleton):
    
    def __init__(self):
        self.clientList = {} # key: django_id, value: client

    def addClient(self, django_id,client):
        self.clientList[django_id] = client
    def getClient(self, django_id):
        return self.clientList[django_id]
    def removeClient(self, django_id):
        del self.clientList[django_id]

# class Organization(models.Model):
#     orgName = models.CharField(max_length=100)
#     orgOwner = models.CharField(max_length=100)
#     def __str__(self):
#         return self.name

             
    
