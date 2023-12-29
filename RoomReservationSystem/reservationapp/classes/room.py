# start = datetime.datetime(2022, 1, 1, 9, 0, 0) # January 1st, 2022 at 9:00 AM
# end = datetime.datetime(2022, 1, 1, 10, 0, 0) # January 1st, 2022 at 10:00 AM
import uuid


class Room:
    # Create
    def __init__(self, name, x, y, capacity, working_hours, permissions):
        self.id = uuid.uuid4()
        self.name = name
        self.x = x
        self.y = y
        self.capacity = capacity
        self.working_hours = working_hours
        #Permissions is dict that maps the users to room CRUD operations {user_id: [PermissionList]}
        self.permissions = permissions
        

    # Delete
    def __del__(self):
        print(f"Room {self.name} deleted")

    # Read
    def getId(self):
        return self.id

    def getName(self):
        return self.name

    def getX(self):
        return self.x

    def getY(self):
        return self.y

    def getCapacity(self):
        return self.capacity

    def getWorkingHours(self):
        return self.working_hours

    def getPermissions(self):
        return self.permissions
    
    def getUserPermissions(self, user_id):
        return self.permissions[user_id]

    # Update
    def updateRoom(self, name, x, y, capacity, working_hours, permissions):
        self.name = name
        self.x = x
        self.y = y
        self.capacity = capacity
        self.working_hours = working_hours
        self.permissions = permissions

    def updatePermissions(self, permissions):
        self.permissions = permissions
    
    def updateUserPermissions(self, user_id, permissions):
        self.permissions[user_id] = permissions    

    def __str__(self):
        return f"Room name: {self.name} Room coord x: {self.x} Room coord y: {self.y} Room capacity: {self.capacity} Room working hours: {self.working_hours}"

    def __repr__(self):
        return f'Room(Id:\'{self.id}\',Name:\'{self.name}\',x,y: {self.x},{self.y},Capacity: {self.capacity},Working hours:({self.working_hours[0].strftime("%H:%M")}),({self.working_hours[1].strftime("%H:%M")}),Permissions:{self.permissions})'
