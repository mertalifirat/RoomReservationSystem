class Room:
    event = None
    def __init__(self,name,x,y,capacity,working_hours,permissions):
        self.name = name
        self.x = x
        self.y = y
        self.capacity = capacity
        self.working_hours = working_hours
        self.permissions = permissions
    def getName(self):
        return self.name
    def getXCoord(self):
        return self.x
    def getYCoord(self):
        return self.y
    def getCapacity(self):
        return self.capacity
    def getWorkingHours(self):
        return self.working_hours
    def getPermissions(self):
        return self.permissions
    def getEvent(self):
        return self.event
    def setEvent(self,event):
        self.event = event
    def roomAvailable(self,start,end):
        if self.getWorkingHours()[0].day == start.day and self.getWorkingHours()[0].month == start.month:
            if start >= self.getWorkingHours()[0] and end <= self.getWorkingHours()[1]:
               return True
        return False
    def __str__(self):
        return f'Room name: {self.name} Room coord x: {self.x} Room coord y: {self.y} Room capacity: {self.capacity} Room working hours: {self.working_hours}'
    def __repr__(self):
        return f'Room(\'{self.name}\', {self.x},{self.y},{self.capacity},({self.working_hours[0].strftime("%Y-%m-%d, %H:%M")}),({self.working_hours[1].strftime("%Y-%m-%d, %H:%M")}),{self.permissions},{repr(self.event)})'    