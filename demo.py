import cmd
from classes import *
import datetime
from classes.room import Room
from classes.event import Event
from classes.organization import Organization
from classes.view import View
from datetime import datetime


class RoomReservationSystemDemo(cmd.Cmd):
    intro = "Welcome to the Demo of the Room Reservation System. Type help or ? to list commands.\n"
    # simple data

    room1 = Room(
        "Room 1",
        0,
        0,
        30,
        (datetime(2020, 1, 1, 8, 0), datetime(2020, 1, 1, 18, 0)),
        ["admin", "user"],
    )
    room2 = Room(
        "Room 2",
        1,
        0,
        20,
        (datetime(2020, 2, 2, 8, 0), datetime(2020, 2, 2, 18, 0)),
        ["admin", "user"],
    )
    room3 = Room(
        "Room 3",
        0,
        1,
        30,
        (datetime(2020, 3, 3, 8, 0), datetime(2020, 3, 3, 18, 0)),
        ["admin", "user"],
    )
    room4 = Room(
        "Room 4",
        1,
        1,
        40,
        (datetime(2020, 4, 4, 8, 0), datetime(2020, 4, 4, 18, 0)),
        ["admin", "user"],
    )

    event1 = Event(
        "Event 1",
        "Event 1 description",
        "Event 1 category",
        10,
        60,
        None,
        ["admin", "user"],
    )
    event2 = Event(
        "Event 2",
        "Event 2 description",
        "Event 2 category",
        20,
        60,
        None,
        ["admin", "user"],
    )
    event3 = Event(
        "Event 3",
        "Event 3 description",
        "Event 3 category",
        30,
        60,
        None,
        ["admin", "user"],
    )

    map = [[None for _ in range(3)] for _ in range(3)]

    organization = Organization(
        "Doruk", "Organization 1", map
    )  # Create a 2D array with None values

    eventList = [event1, event2, event3]
    organization.addRoom(room1)
    organization.addRoom(room2)
    organization.addRoom(room3)
    organization.addRoom(room4)

    organization.addEvent(event1)
    organization.addEvent(event2)
    organization.addEvent(event3)

    view = View("Doruk")

    def do_add_room(self, arg):
        """Add a room to the organization: add_room name x y capacity start end permissions"""
        # pdb.set_trace()
        arg = arg.split(" ")
        name = arg[0]
        x = int(arg[1])
        y = int(arg[2])
        capacity = int(arg[3])
        start = datetime.strptime(arg[4], "%Y-%m-%d-%H:%M")
        end = datetime.strptime(arg[5], "%Y-%m-%d-%H:%M")
        permissions = arg[6].split(",")
        room = Room(name, x, y, capacity, (start, end), permissions)
        self.organization.addRoom(room)
        print(f"Room {name} added to the organization")

    def do_add_event(self, arg):
        """Add an event to the organization: add_event title description category capacity duration permissions"""
        arg = arg.split(" ")
        title = arg[0]
        description = arg[1]
        category = arg[2]
        capacity = int(arg[3])
        duration = int(arg[4])
        permissions = arg[5].split(",")
        event = Event(
            title, description, category, capacity, duration, None, permissions
        )
        self.organization.addEvent(event)
        print(f"Event {title} added to the organization")

    def do_reserve_example(self, arg):
        """Reserve an event to a room: reserve starttime
        for now event1 reserves room1 examples is shown"""
        arg = arg.split(" ")
        start = datetime.strptime(arg[0], "%Y-%m-%d-%H:%M")
        self.organization.reserve(self.event1, self.room1, start)
        print(self.organization.eventList[self.event1.getId()][1])

    # def query(self, title, category, rect=None, room=None)
    def do_query_example(self, arg):
        """Query the organization: query title category
        example: query title1 category1
        for now rect and room are disabled
        room1 is used as room"""
        arg = arg.split(" ")
        title = arg[0]
        category = arg[1]
        # rect = arg[2].split(",")
        # rect = tuple(map(int, rect))
        # room = arg[3]

        ## example for room1
        for i in self.organization.query(title, category, None, self.room1):
            print(i)

        print(f"do_query_example done")

    def do_print_organization(self, arg):
        """Print the organization: print_organization"""
        print(self.organization)

    def do_find_room_example(self, arg):
        """Find a room in the organization: find_room rect start end"""
        arg = arg.split(" ")
        rect = arg[0].split(",")
        rect = tuple(map(int, rect))

        start = datetime.strptime(arg[1], "%Y-%m-%d-%H:%M")
        end = datetime.strptime(arg[2], "%Y-%m-%d-%H:%M")
        event = self.event1
        roomListIter = self.organization.findRoom(event, rect, start, end)
        for room in roomListIter:
            print(room)

    def do_find_schedule_example(self, arg):
        """Find a schedule for all events in the event list: find_schedule rect start end"""
        arg = arg.split(" ")
        rect = arg[0].split(",")
        rect = tuple(map(int, rect))
        start = datetime.strptime(arg[1], "%Y-%m-%d-%H:%M")
        end = datetime.strptime(arg[2], "%Y-%m-%d-%H:%M")
        eventList = self.eventList
        schedule = self.organization.findSchedule(eventList, rect, start, end)
        for key, values in schedule.items():
            print(self.organization.getEvent(key))
            for e in values:
                print(e)

    def do_reassign_example(self, arg):
        """Reassign an event to a given room: reassign
        for simplicity event1 is used as event and room1 is used as room"""
        event = self.event1
        room = self.room2
        self.organization.reassign(event, room)
        print(f"Event {event} reassigned to room {room}")

    def do_add_query_example(self, arg):
        """Add a query to the view: add_query title category rect
        room is assigned"""
        arg = arg.split(" ")
        organization = self.organization
        title = arg[0]
        category = arg[1]
        rect = arg[2].split(",")
        rect = tuple(map(int, rect))
        room = self.room1
        self.view.addQuery(organization, title, category, rect, room)
        print(f"Query added to the view")

    def do_room_view_example(self, arg):
        """View the rooms in the organization: room_view start end"""
        arg = arg.split(" ")
        start = datetime.strptime(arg[0], "%Y-%m-%d-%H:%M")
        end = datetime.strptime(arg[1], "%Y-%m-%d-%H:%M")
        rooms = self.view.roomView(start, end)
        for key, values in rooms.items():
            print(key)
            for e in values:
                print(e)

    def do_day_view_example(self, arg):
        """View the days in the organization: day_view start end"""
        arg = arg.split(" ")
        start = datetime.strptime(arg[0], "%Y-%m-%d-%H:%M")
        end = datetime.strptime(arg[1], "%Y-%m-%d-%H:%M")
        days = self.view.dayView(start, end)
        for key, values in days.items():
            print(key)
            for e in values:
                print(e)

    def do_bye(self, arg):
        """Exit the program: bye"""
        print("Thank you for using RoomReservationSystemDemo")
        return True


if __name__ == "__main__":
    RoomReservationSystemDemo().cmdloop()
