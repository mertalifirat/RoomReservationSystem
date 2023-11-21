from .event import Event
from .room import Room
from datetime import datetime, timedelta
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
        result = f"Organization name: {self.name} Organization owner: {self.owner} Organization map: {self.map}\n"

        for key in self.roomList:
            result += f"{self.roomList[key]}\n"
        for key in self.eventList:
            result += f"{self.eventList[key]}\n"
        return result

    def addRoom(self, room):
        x = room.getX()
        y = room.getY()
        self.map[x][y] = room
        self.roomList[room.getId()] = [room, None]  # None means room is not reserved

    def addEvent(self, event):
        self.eventList[event.getId()] = [
            event,
            None,
        ]  # None means event is not reserved

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

    def updateEvent(self, id, title, description, category, capacity, duration, weekly):
        event = self.getEvent(id)
        event.updateEvent(title, description, category, capacity, duration, weekly)

    # Delete
    def deleteEvent(self, id):
        self.eventList.pop(id)

    def deleteRoom(self, id):
        self.roomList.pop(id)

    # Reserve the room for the event if room is available and conditions are satisfied
    def reserve(self, event, room, start):
        # If the room is available
        if self.roomList[room.getId()][1] == None:
            end = start + timedelta(minutes=event.getDuration())
            # If the room is available at the given time
            if room.roomAvailable(start, end):
                # If the room has enough capacity
                if room.getCapacity() >= event.getCapacity():
                    self.roomList[room.getId()][1] = event.getId()
                    self.eventList[event.getId()][1] = room.getId()

    # Return available rooms iterator for the given event and rectangle
    def findRoom(self, event, rect, start, end):
        x, y, w, h = rect
        available_rooms = []

        # Assuming top left and top right coordinates are not included
        for i in range(w):
            for j in range(h):
                room = self.map[x + i][y + j]
                if (
                    room.roomAvailable(start, end)
                    and self.roomList[room.getId()][1] == None
                ):
                    if room.getCapacity() >= event.getCapacity():
                        available_rooms.append(room)

        return iter(available_rooms)

    # Return a dictionary of keys are event ids and values are available rooms iterator for the given event list and rectangle
    def findSchedule(self, eventlist, rect, start, end):
        result = {}
        for _, event in eventlist.items():
            result[event[0].getId()] = self.findRoom(event, rect, start, end)
        return result

    # Reassign the event to the room if room is available and conditions are satisfied
    def reassign(self, event, room):
        oldRoomId = self.getRoom(self.eventList[event.getId()][1])

        if (
            room.roomAvailable(event.getStartTime(), event.getEndTime())
            and room.getCapacity() >= event.getCapacity()
            and self.roomList[room.getId()][1] == None
        ):
            self.roomList[oldRoomId][1] = None
            self.roomList[room.getId()][1] = event.getId()
            self.eventList[event.getId()][1] = room.getId()

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
                    value.getX() >= x
                    and value.getX() <= x + w
                    and value.getY() >= y
                    and value.getY() <= y + h
                ):
                    roomResult.append(value)
            for _, event in eventResult.items():
                for value in roomResult:
                    start = value.getWorkingHours()[0]
                    end = start + timedelta(minutes=event.getDuration())
                    if (
                        value.roomAvailable(start, end)
                        and value.getCapacity() >= event.getCapacity()
                        and self.roomList[value.getId()][1] == None
                    ):
                        queryResult.append(event, value, start)
        elif room != None:
            start = room.getWorkingHours()[0]
            for event in eventResult:
                end = start + timedelta(minutes=event.getDuration())
                if (
                    room.roomAvailable(start, end)
                    and room.getCapacity() >= event.getCapacity()
                    and self.roomList[room.getId()][1] == None
                ):
                    queryResult.append((event, room, start))
        return queryResult
