from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone
# Create your models here.
import datetime
import pytz

utc = pytz.UTC

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

class Organization(models.Model):
    class Meta:
        ordering = ['orgName']
    orgServerId = models.CharField(max_length=100)
    orgName = models.CharField(max_length=100)
    orgOwner = models.CharField(max_length=100)

class Room(models.Model):
    class Meta:
        ordering = ['roomName']
    roomId = models.CharField(max_length=100)
    roomName = models.CharField(max_length=100)
    roomCapacity = models.IntegerField(default=0)
    roomWorkingHours = models.CharField(max_length=100)


             
    
