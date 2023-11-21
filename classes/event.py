import uuid


class Event:
    # Create
    def __init__(
        self, title, description, category, capacity, duration, weekly, permissions
    ):
        self.id = uuid.uuid4()
        self.title = title
        self.description = description
        self.category = category
        self.capacity = capacity
        self.duration = duration
        self.weekly = weekly
        self.permissions = permissions

    # Delete
    def __del__(self):
        print(f"Event {self.title} deleted")

    # Read
    def getId(self):
        return self.id

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

    # Update
    def updateEvent(
        self, title, description, category, capacity, duration, weekly, permissions
    ):
        self.title = title
        self.description = description
        self.category = category
        self.capacity = capacity
        self.duration = duration
        self.weekly = weekly
        self.permissions = permissions

    def __str__(self):
        return f"Event title: {self.title} Event description: {self.description} Event category: {self.category} Event capacity: {self.capacity} Event duration: {self.duration} Event weekly:{self.weekly}"

    def __repr__(self):
        return f"Event('{self.title}', {self.description},{self.category},{self.capacity},{self.duration},{self.weekly},{self.permissions})"
