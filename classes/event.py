from datetime import datetime


class Event:
    room = None

    def __init__(
        self, title, description, category, capacity, duration, weekly, permissions
    ):
        self.title = title
        self.description = description
        self.category = category
        self.capacity = capacity
        self.duration = duration
        self.weekly = weekly
        self.permissions = permissions

    def getTitle(self):
        return self.title

    def getDescription(self):
        return self.description

    def getCategory(self):
        return self.category

    def getCapacity(self):
        return self.capacity

    def getDuration(self):
        return self.duration

    def getWeekly(self):
        return self.weekly

    def getPermissions(self):
        return self.permissions

    def getRoom(self):
        return self.room

    def setRoom(self, room):
        self.room = room

    def __str__(self):
        return f"Event title: {self.title} Event description: {self.description} Event category: {self.category} Event capacity: {self.capacity} Event duration: {self.duration} Event weekly:{self.weekly}"

    def __repr__(self):
        return f"Event('{self.title}', {self.description},{self.category},{self.capacity},{self.duration},{self.weekly},{self.permissions})"
