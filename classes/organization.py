from collections import OrderedDict
from event import Event
from room import Room
from datetime import datetime, timedelta


class Organization:
    room_list = OrderedDict()
    room_index = 0

    def __init__(self, owner, name, map):
        self.owner = owner
        self.name = name
        self.map = map

    def getOwner(self):
        return self.owner

    def getName(self):
        return self.name

    def getName(self):
        return self.map

    def updateOrganization(self, owner, name, map):
        self.owner = owner
        self.name = name
        self.map = map

    def addRoom(self, room):
        self.room_list[self.room_index] = room
        self.room_index += 1

    def getRoom(self, id):
        return self.room_list.get(id)

    def updateRoom(self, id, name, x, y, capacity, working_hours, permissions):
        room = Room(id, name, x, y, capacity, working_hours, permissions)
        self.room_list.update(room)

    def deleteRoom(self, id):
        self.room_list.pop(id)

    def reserve(self, event, room, start):
        end = start + timedelta(minutes=event.getDuration())
        if room.roomAvailable(start, end):
            if room.getEvent == None:
                room.setEvent(event)
                event.setRoom(room)

    def findRoom(self, event, rect_x, rect_y, start, end):
        available_rooms = []
        for key in self.room_list:
            room = self.getRoom(key)
            if room.roomAvailable(start, end):
                if room.getCapacity() >= event.getCapacity():
                    if room.getXCoord() >= rect_x and room.getYCoord() >= rect_y:
                        available_rooms.append(room)
        return available_rooms
        # return iter(available_rooms)

    def reassign(event, room):
        if room.getEvent == None:
            event.getRoom().setEvent = None
            event.setRoom(room)
            room.setEvent(event)


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
