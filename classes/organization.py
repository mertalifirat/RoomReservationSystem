from .event import Event
from .room import Room
from datetime import datetime, timedelta,time
import uuid
from collections import OrderedDict
import pdb


class Organization:
    # Create
    def __init__(self, owner, name, map):
        self.id = uuid.uuid4()
        self.owner = owner
        self.name = name
        self.map = map
        self.roomList = OrderedDict()
        self.eventList = OrderedDict()

    def __repr__(self):
        result = f"Organization name: {self.name} \n Organization owner: {self.owner} \n Organization map: {self.map}\n"

        for key in self.roomList:
            result += f"{self.roomList[key]}\n"
        for key in self.eventList:
            result += f"{self.eventList[key]}\n"
        return result

    def addRoom(self, room):
        x = room.getX()
        y = room.getY()
        self.map[x][y] = room
        self.roomList[room.getId()] = [room, []]  # First item is room object, second is list of (eventId,starttime,endtime) tuples

    def addEvent(self, event):
        self.eventList[event.getId()] = [
            event,
            None,
        ]  # First item is event object, second is roomId that event is reserved

    # Read
    def getId(self):
        return self.id
    
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

    def updateEvent(self, id, title, description, category, capacity, duration, weekly):
        event = self.getEvent(id)
        event.updateEvent(title, description, category, capacity, duration, weekly)

    # Delete
    def deleteEvent(self, id):
        self.eventList.pop(id)

    def deleteRoom(self, id):
        self.roomList.pop(id)

    #Check if the room is available between given dates, for that we are getting hour and minute from eventStart and eventEnd
    def isRoomAvailableBetweenHours(self, room, eventStart,eventEnd):
        #Room doesn't have any reservations
        if self.roomList[room.getId()][1]:
            #Check if room is working for event duration
            eventStartHourMinute = time(eventStart.hour,eventStart.minute)
            eventEndHourMinute = time(eventEnd.hour,eventEnd.minute)
            if room.getWorkingHours()[0] <= eventStartHourMinute and room.getWorkingHours()[1] >= eventEndHourMinute:
                return True
        else:
            #Check if there is no collisions with other events in the room
            for eventId,starttime,endtime in self.roomList[room.getId()][1]: 
                if eventStart <= starttime or eventStart < endtime:
                    if eventEnd < starttime or eventEnd <= endtime:
                        return False
            return True      
    # Reserve the room for the event if room is available and conditions are satisfied
    def reserve(self, event, room, start):
        #Calculate end time for given event
        end = start + timedelta(minutes=event.getDuration())
        # If the room is available at the given time
        if self.isRoomAvailableBetweenHours(room,start,end):
            # If the room has enough capacity add event to the room reservation list and add room to the event room list
            if room.getCapacity() >= event.getCapacity():
                #Check if event is weekly or not
                if event.getWeekly() is None:
                    self.roomList[room.getId()][1].append((event.getId(),start,end))
                    self.eventList[event.getId()][1] = room.getId()
                #If event is weekly add event to the room reservation list for every week
                #TODO: Check if room has PERWRITE permission
                else:
                    while start < event.getWeekly():
                        self.roomList[room.getId()][1].append((event.getId(),start,end))
                        self.eventList[event.getId()][1] = room.getId()
                        start += timedelta(days=7)
                        end += timedelta(days=7)   

    # Return available rooms iterator for the given event and rectangle
    def findRoom(self, event, rect, start, end):
        x, y, w, h = rect
        available_rooms = []

        # Assuming top left and top right coordinates are not included
        for i in range(w):
            for j in range(h):
                #Checking if there is a room in the given coordinates
                if self.map[x + i][y + j] == None:
                    continue
                else:
                    room = self.map[x + i][y + j]
                    if (
                        self.isRoomAvailableBetweenHours(start, end) and room.getCapacity() >= event.getCapacity()
                    ):
                        available_rooms.append(room)

        return iter(available_rooms)

    # Return a dictionary of keys are event ids and values are available rooms iterator for the given event list and rectangle
    def findSchedule(self, eventlist, rect, start, end):
        result = {}
        for event in eventlist:
            result[event.getId()] = self.findRoom(event, rect, start, end)
        return result

    # Reassign the event to the room if room is available and conditions are satisfied
    def reassign(self, event, room):
        #Getting [room,[eventId,starttime,endttime]] of old room
        oldRoomId = self.eventList[event.getId()][1]
        #Check if the event is already reserved a room
        if oldRoomId is not None:
            oldRoom = self.roomList[oldRoomId]
            #Getting event start time and end time
            eventTuple= ()
            for eventId,start,end in oldRoom[1]:
                print(eventId,start,end)
                if eventId == event.getId():
                    eventTuple = (eventId,start,end)
                    break
            eventId = event.getId()    
            starttime = eventTuple[1]
            endtime = eventTuple[2]
            #Checking if new room is available
            if self.isRoomAvailableBetweenHours(room,starttime,endtime):
                if room.getCapacity() >= event.getCapacity():
                    #If event is not weekly
                    if event.getWeekly() is None:
                        #Removing event from old room
                        oldRoom[1].remove((eventId,starttime,endtime))
                        #Adding event to new room
                        self.roomList[room.getId()][1].append((eventId,starttime,endtime))
                    #If event is weekly    
                    else:    
                        while starttime < event.getWeekly():
                            #Removing event from old room
                            oldRoom[1].remove((eventId,starttime,endtime))
                            #Adding event to new room
                            self.roomList[room.getId()][1].append((eventId,starttime,endtime))
                            starttime += timedelta(days=7)
                            endtime += timedelta(days=7)
                    #Updating event room
                    self.eventList[event.getId()][1] = room.getId()

    #Needs to be changed
    def query(self, title, category, rect=None, room=None):
        queryResult = []
        roomResult = []
        eventResult = []
        # Matching events with title and category
        for _, event in self.eventList.items():
            if title in event[0].getTitle() and category in event[0].getCategory():
                eventResult.append(event[0])
        if rect != None:
            x, y, w, h = rect
            # Matching rooms with given rectangle
            for _, value in self.roomList.items():
                if (
                    value[0].getX() >= x
                    and value[0].getX() <= x + w
                    and value[0].getY() >= y
                    and value[0].getY() <= y + h
                ):
                    #Append room,[(eventId,starttime,endtime)]
                    roomResult.append(value)
            for event in eventResult:
                for value in roomResult:
                    start = value.getWorkingHours()[0]
                    end = start + timedelta(minutes=event.getDuration())
                    if (
                        room.getWorkingHours()[0] <= start
                        and end <= room.getWorkingHours()[1]
                        and value.getCapacity() >= event.getCapacity()
                        and self.roomList[value.getId()][1] == None
                    ):
                        queryResult.append((event, value, start))
        elif room != None:
            start = room.getWorkingHours()[0]
            for event in eventResult:
                end = start + timedelta(minutes=event.getDuration())
                if (
                    room.getWorkingHours()[0] <= start
                    and end <= room.getWorkingHours()[1]
                    and room.getCapacity() >= event.getCapacity()
                    and self.roomList[room.getId()][1] == None
                ):
                    queryResult.append((event, room, start))
        return queryResult
