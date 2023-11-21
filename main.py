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
    rows = 3
    cols = 4
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

    print(organization.query("Event 1", "Event 1 category", rect=None, room=room1))


if __name__ == "__main__":
    demo()
