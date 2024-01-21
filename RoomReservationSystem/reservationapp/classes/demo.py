import cmd
from datetime import time
import uuid
import datetime
from room import Room
from user import User
from event import Event
from organization import Organization
from view import View
from datetime import datetime
import pickle
from singletonCatalgoue import Catalogue


# {uuid.UUID("24a6ad2b-4e27-4e37-9d2a-1aabc7ea52fc"):["LIST","RESERVE","DELETE"],uuid.UUID("bb1e0182-e1f3-4c02-9d6c-dee14d75caf1"):["DELETE"]}
class RoomReservationSystemDemo(cmd.Cmd):
    intro = "Welcome to the Demo of the Room Reservation System. Type help or ? to list commands.\n"
    # simple data

    room1 = Room(
        "Room 1",
        39.89413109880857,
        32.77663707733155,
        30,
        (time(8, 0), time(18, 0)),
        {
            uuid.UUID("e3a7d696-6660-4f7b-ae22-8c0664472e4c"): [
                "LIST",
                "RESERVE",
                "DELETE",
            ],
            uuid.UUID("bb1e0182-e1f3-4c02-9d6c-dee14d75caf1"): [
                "LIST",
                "RESERVE",
                "DELETE",
            ],
        },
    )
    room2 = Room(
        "Room 2",
        39.89513109880857,
        32.77763707733155,
        20,
        (time(8, 0), time(18, 0)),
        {
            uuid.UUID("e3a7d696-6660-4f7b-ae22-8c0664472e4c"): [
                "LIST",
                "RESERVE",
                "DELETE",
            ],
            uuid.UUID("bb1e0182-e1f3-4c02-9d6c-dee14d75caf1"): [
                "LIST",
                "RESERVE",
                "DELETE",
            ],
        },
    )
    room3 = Room(
        "Room 3",
        39.89613109880857,
        32.77863707733155,
        30,
        (time(8, 0), time(18, 0)),
        {
            uuid.UUID("e3a7d696-6660-4f7b-ae22-8c0664472e4c"): [
                "LIST",
                "RESERVE",
                "DELETE",
            ],
            uuid.UUID("bb1e0182-e1f3-4c02-9d6c-dee14d75caf1"): [
                "LIST",
                "RESERVE",
                "DELETE",
            ],
        },
    )
    room4 = Room(
        "Room 4",
        39.89713109880857,
        32.77963707733155,
        40,
        (time(8, 0), time(18, 0)),
        {
            uuid.UUID("e3a7d696-6660-4f7b-ae22-8c0664472e4c"): [
                "LIST",
                "RESERVE",
                "DELETE",
            ],
            uuid.UUID("bb1e0182-e1f3-4c02-9d6c-dee14d75caf1"): [
                "LIST",
                "RESERVE",
                "DELETE",
            ],
        },
    )

    event1 = Event(
        "Event 1",
        "Event 1 description",
        "Event 1 category",
        10,
        60,
        None,
        # datetime(2022,2,1),
        {
            uuid.UUID("e3a7d696-6660-4f7b-ae22-8c0664472e4c"): ["READ", "WRITE"],
            uuid.UUID("bb1e0182-e1f3-4c02-9d6c-dee14d75caf1"): ["READ", "WRITE"],
        },
    )
    event2 = Event(
        "Event 2",
        "Event 2 description",
        "Event 2 category",
        20,
        70,
        None,
        {
            uuid.UUID("e3a7d696-6660-4f7b-ae22-8c0664472e4c"): ["READ", "WRITE"],
            uuid.UUID("bb1e0182-e1f3-4c02-9d6c-dee14d75caf1"): ["READ", "WRITE"],
        },
    )
    event3 = Event(
        "Event 3",
        "Event 3 description",
        "Event 3 category",
        30,
        60,
        None,
        {
            uuid.UUID("e3a7d696-6660-4f7b-ae22-8c0664472e4c"): ["READ", "WRITE"],
            uuid.UUID("bb1e0182-e1f3-4c02-9d6c-dee14d75caf1"): ["READ", "WRITE"],
        },
    )

    # map = [[None for _ in range(3)] for _ in range(3)]

    organization = Organization(
        "Doruk",
        "Organization 1",
        map,
        {
            uuid.UUID("e3a7d696-6660-4f7b-ae22-8c0664472e4c"): [
                "LIST",
                "ADD",
                "ACCESS",
            ],
            uuid.UUID("bb1e0182-e1f3-4c02-9d6c-dee14d75caf1"): [
                "LIST",
                "ADD",
                "ACCESS",
            ],
        },
    )  # Create a 2D array with None values

    organization2 = Organization(
        "Mert",
        "Organization 2",
        map,
        {
            uuid.UUID("e3a7d696-6660-4f7b-ae22-8c0664472e4c"): [
                "LIST",
                "ADD",
                "ACCESS",
            ],
            uuid.UUID("bb1e0182-e1f3-4c02-9d6c-dee14d75caf1"): [
                "LIST",
                "ADD",
                "ACCESS",
            ],
        },
    )  # Create a 2D array with None values

    organization3 = Organization(
        "Ece",
        "Organization 3",
        map,
        {
            uuid.UUID("e3a7d696-6660-4f7b-ae22-8c0664472e4c"): [
                "LIST",
                "ADD",
                "ACCESS",
            ],
            uuid.UUID("bb1e0182-e1f3-4c02-9d6c-dee14d75caf1"): [
                "LIST",
                "ADD",
                "ACCESS",
            ],
        },
    )  # Create a 2D array with None values

    eventList = [event1, event2, event3]
    organization.addRoom(room1)
    organization.addRoom(room2)
    organization.addRoom(room3)
    organization.addRoom(room4)

    organization.addEvent(event1)
    organization.addEvent(event2)
    organization.addEvent(event3)

    user1 = User("doruk", "doruk@localhost.com", "doruko", "mert1234")
    user1.update_userId(uuid.UUID("e3a7d696-6660-4f7b-ae22-8c0664472e4c"))
    user2 = User("mert", "mert@localhost.com", "mert", "doruk1234")
    user2.update_userId(uuid.UUID("bb1e0182-e1f3-4c02-9d6c-dee14d75caf1"))
    catalogue = Catalogue()
    catalogue.addUser(user1)
    catalogue.addUser(user2)
    catalogue.addOrganization(organization)
    catalogue.addOrganization(organization2)
    catalogue.addOrganization(organization3)

    view = View("Doruk")

    def __del__(self):
        print("Server shutdown, file saved")
        print(self.catalogue.getOrganizationList())
        print(self.catalogue.getUserList())
        pickle.dump(self.catalogue, open("organizations.p", "wb"))

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
        start1 = datetime.strptime(arg[0], "%Y-%m-%d-%H:%M")
        start2 = datetime.strptime(arg[1], "%Y-%m-%d-%H:%M")
        self.organization.reserve(self.event1, self.room1, start1)
        self.organization.reserve(self.event2, self.room1, start2)
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
