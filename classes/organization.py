from event import Event
from room import Room
from datetime import datetime, timedelta
import uuid
from collections import OrderedDict


class Organization:
    def __init__(self, owner, name, map):
        self.owner = owner
        self.name = name
        self.map = map
        self.roomList = OrderedDict()
        self.eventList = OrderedDict()

    # Create
    def addRoom(self, room):
        self.map[room.getX()][room.getY()] = room
        self.roomList[room.getId()] = [room, None] # None means room is not reserved

    def addEvent(self, event):
        self.eventList[event.getId()] = [event, None] # None means event is not reserved

    # Read
    def getOwner(self):
        return self.owner

    def getName(self):
        return self.name

    def getMap(self):
        return self.map

    def getRoomList(self):
        return self.roomList

    def getEventList(self):
        return self.eventList

    def getRoom(self, id):
        return self.roomList.get(id)

    def getEvent(self, id):
        return self.eventList.get(id)

    # Update
    def updateOrganization(self, owner, name, map):
        self.owner = owner
        self.name = name
        self.map = map

    def updateOwner(self, owner):
        self.owner = owner

    def updateName(self, name):
        self.name = name

    def updateMap(self, map):
        self.map = map

    def updateRoom(self, id, name, x, y, capacity, working_hours, permissions):
        self.map[room.getX()][room.getY()] = None
        room = self.getRoom(id)
        room.updateRoom(name, x, y, capacity, working_hours, permissions)
        self.map[room.getX()][room.getY()] = room

    def deleteRoom(self, id):
        del self.roomList.pop(id)

    def updateEvent(self, id, title, description, category, capacity, duration, weekly):
        event = self.getEvent(id)
        event.updateEvent(title, description, category, capacity, duration, weekly)

    def deleteEvent(self, id):
        del self.eventList.pop(id)

    def reserve(self, event, room, start):
        # If the room is available
        if (self.roomList[room.getId()][1] == None):
            end = start + timedelta(minutes=event.getDuration())
            # If the room is available at the given time
            if room.roomAvailable(start, end):
                # If the room has enough capacity
                if room.getCapacity() >= event.getCapacity():
                    self.roomList[room.getId()][1] = event.getId()
                    self.eventList[event.getId()][1] = room.getId()
                    
    def findRoom(self, event, rect, start, end):
        x,y,w,h = rect
        available_rooms = []

        # Assuming top left and top right coordinates are not included 
        for i in range(w):
            for j in range(h):
                room = self.map[x+i][y+j]
                if room.roomAvailable(start, end) and self.roomList[room.getId()][1] == None:
                    if room.getCapacity() >= event.getCapacity():
                        available_rooms.append(room)

        return iter(available_rooms)
    
    # Assigning available rooms iterator to given events
    def findSchedule(self, eventlist, rect, start, end):
        result = {}
        for event in eventlist:
            result[event.getId()] = self.findRoom(event, rect, start, end)
        return result
        

    def reassign(self, event, room):

        oldRoomId = self.getRoom(self.eventList[event.getId()][1])

        if (room.roomAvailable(event.getStartTime(), event.getEndTime()) and room.getCapacity() >= event.getCapacity() and self.roomList[room.getId()][1] == None):
            self.roomList[oldRoomId][1] = None
            self.roomList[room.getId()][1] = event.getId()
            self.eventList[event.getId()][1] = room.getId()
        
    def query(self,  title, category, rect=None, room=None):
        queryResult = []
        roomResult = []
        eventResult = []
        for event in self.eventList:
            if (title in event.getTitle() and category in event.getCategory()):
                eventResult.append(event)
        if (rect != None):
            x,y,w,h = rect
            for room in self.roomList:
                if(room.getX() >= x and room.getX() <= x+w and room.getY() >= y and room.getY() <= y+h):
                    roomResult.append(room)
            for event in eventResult:
                for room in roomResult:
                    start = room.getWorkingHours()[0]
                    end = start + timedelta(minutes=event.getDuration())
                    if (room.roomAvailable(start, end) and room.getCapacity() >= event.getCapacity() and self.roomList[room.getId()][1] == None):
                        queryResult.append(event,room,start)   
        elif (room != None):
            start = room.getWorkingHours()[0]
            for event in eventResult:
                end = start + timedelta(minutes=event.getDuration())
                if (room.roomAvailable(start, end) and room.getCapacity() >= event.getCapacity() and self.roomList[room.getId()][1] == None):
                    queryResult.append(event,room,start)
        return queryResult            
                    

    

room = Room(
    "A", 1, 2, 100, [datetime(2023, 10, 20, 19, 00), datetime(2023, 10, 20, 20, 00)], 1
)
room2 = Room(
    "B", 1, 2, 200, [datetime(2023, 10, 20, 19, 00), datetime(2023, 10, 20, 20, 10)], 1
)
event = Event("Game", "Football match", "Sports", 150, 50, None, 1)
# print(repr(event))
organization = Organization("doruk", "saracoglu", "map")
organization.addRoom(room)
organization.addRoom(room2)
# print(repr(organization.findRoom(event,1,2,datetime(2023,10,20,19,00),datetime(2023,10,20,20,10))))
organization.reserve(event, room, datetime(2023, 10, 20, 19, 00))
print(repr(room))
