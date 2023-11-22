import sys
from classes.room import Room
from classes.event import Event
from classes.organization import Organization
from datetime import datetime, timedelta


def demo():
    room1 = Room(
        "Room 1",
        0,
        0,
        100,
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

    # example map for testing 2D array
    rows = 5
    cols = 5
    map = [[None for _ in range(cols)] for _ in range(rows)]

    organization = Organization(
        "Doruk", "Organization 1", map
    )  # Create a 2D array with None values

    organization.addRoom(room1)
    organization.addRoom(room2)
    organization.addRoom(room3)
    organization.addRoom(room4)

    organization.addEvent(event1)
    organization.addEvent(event2)
    organization.addEvent(event3)
    print(organization)
    organization.reserve(event1, room1, datetime(2020, 1, 1, 8, 0))
    print(organization)
    organization.findRoom(
        event1,
        (
            0,
            0,
            1,
            1,
        ),
        datetime(2020, 1, 1, 8, 0),
        datetime(2020, 1, 1, 10, 0),
    )

    # while True:
    #     command = input("Enter a command (q to quit): ")
    #     if command == "q":
    #         break
    #     elif command == "query":
    #         event_name = input("Enter event name: ")
    #         event_category = input("Enter event category: ")
    #         room_name = input("Enter room name: ")
    #         room = organization.getRoomByName(room_name)
    #         if room:
    #             result = organization.query(
    #                 event_name, event_category, rect=None, room=room
    #             )
    #             print(result)
    #     elif command == "findRoom":

    #     # elif command == "addRoom":
    #     #     room_name = input("Enter room name: ")
    #     #     room_capacity = int(input("Enter room capacity: "))
    #     #     room_location_x = int(input("Enter room location (x-coordinate): "))
    #     #     room_location_y = int(input("Enter room location (y-coordinate): "))
    #     #     room_availability_start = datetime.strptime(
    #     #         input("Enter room availability start (YYYY,MM,DD,HH,MM): "),
    #     #         "%Y,%m,%d,%H,%M",
    #     #     )
    #     #     room_availability_end = datetime.strptime(
    #     #         input("Enter room availability end (YYYY,MM,DD,HH,MM): "),
    #     #         "%Y,%m,%d,%H,%M",
    #     #     )
    #     #     room_users = input("Enter room users (comma-separated): ").split(",")
    #     #     room = Room(
    #     #         room_name,
    #     #         room_capacity,
    #     #         room_location_x,
    #     #         room_location_y,
    #     #         (room_availability_start, room_availability_end),
    #     #         room_users,
    #     #     )
    #     #     organization.addRoom(room)
    #     #     print("Room added successfully.")

    #     # elif command == "addEvent":
    #     #     event_name = input("Enter event name: ")
    #     #     event_description = input("Enter event description: ")
    #     #     event_category = input("Enter event category: ")
    #     #     event_capacity = int(input("Enter event capacity: "))
    #     #     event_duration = int(input("Enter event duration (minutes): "))
    #     #     event_start_time = datetime.strptime(
    #     #         input("Enter event start time (YYYY,MM,DD,HH,MM): "),
    #     #         "%Y,%m,%d,%H,%M",
    #     #     )
    #     #     event_users = input("Enter event users (comma-separated): ").split(",")
    #     #     event = Event(
    #     #         event_name,
    #     #         event_description,
    #     #         event_category,
    #     #         event_capacity,
    #     #         event_duration,
    #     #         event_start_time,
    #     #         event_users,
    #     #     )
    #     #     organization.addEvent(event)
    #     #     print("Event added successfully.")

    #     elif command == "findRoom":
    #         room_name = input("Enter room name: ")
    #         room = organization.getRoomByName(room_name)
    #         if room:
    #             print(room)
    #         else:
    #             print("Room not found.")

    #     else:
    #         print("Invalid command.")


if __name__ == "__main__":
    demo()
