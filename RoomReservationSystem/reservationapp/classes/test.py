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

#{uuid.UUID("24a6ad2b-4e27-4e37-9d2a-1aabc7ea52fc"):["LIST","RESERVE","DELETE"],uuid.UUID("d7eb60b7-3cd3-41bc-b758-1f76d22e1748"):["DELETE"]}
class RoomReservationSystemDemo(cmd.Cmd):
    intro = "Welcome to the Demo of the Room Reservation System. Type help or ? to list commands.\n"
    # simple data

    room1 = Room(
        "Room 1",
        0,
        0,
        30,
        (time(8, 0), time(18, 0)),
        {},
    )
    room2 = Room(
        "Room 2",
        1,
        0,
        20,
        (time(8, 0), time(18, 0)),
        {uuid.UUID("4629710e-d299-42da-a3e6-09f40b79e356"):["LIST","RESERVE","DELETE"], uuid.UUID("d7eb60b7-3cd3-41bc-b758-1f76d22e1748"):["DELETE"]},
    )
    room3 = Room(
        "Room 3",
        0,
        1,
        30,
        (time(8, 0), time(18, 0)),
        {uuid.UUID("4629710e-d299-42da-a3e6-09f40b79e356"):["LIST","RESERVE","DELETE"], uuid.UUID("d7eb60b7-3cd3-41bc-b758-1f76d22e1748"):["DELETE"]},
    )
    room4 = Room(
        "Room 4",
        1,
        1,
        40,
        (time(8, 0), time(18, 0)),
        {uuid.UUID("4629710e-d299-42da-a3e6-09f40b79e356"):["LIST","RESERVE","DELETE"], uuid.UUID("d7eb60b7-3cd3-41bc-b758-1f76d22e1748"):["DELETE"]},
    )

    event1 = Event(
        "Event 1",
        "Event 1 description",
        "Event 1 category",
        10,
        60,
        None,
        # datetime(2022,2,1),
        {uuid.UUID("4629710e-d299-42da-a3e6-09f40b79e356"):["READ","WRITE"], uuid.UUID("d7eb60b7-3cd3-41bc-b758-1f76d22e1748"):["READ"]},
    )
    event2 = Event(
        "Event 2",
        "Event 2 description",
        "Event 2 category",
        20,
        70,
        None,
        {uuid.UUID("4629710e-d299-42da-a3e6-09f40b79e356"):["READ","WRITE"], uuid.UUID("d7eb60b7-3cd3-41bc-b758-1f76d22e1748"):["READ"]},
    )
    event3 = Event(
        "Event 3",
        "Event 3 description",
        "Event 3 category",
        30,
        60,
        None,
        {uuid.UUID("4629710e-d299-42da-a3e6-09f40b79e356"):["READ","WRITE"], uuid.UUID("d7eb60b7-3cd3-41bc-b758-1f76d22e1748"):["READ"]},
    )

    map = [[None for _ in range(3)] for _ in range(3)]

    organization = Organization(
        "Doruk", "Organization 1", map ,{uuid.UUID("4629710e-d299-42da-a3e6-09f40b79e356") : ["LIST","ADD","ACCESS"], uuid.UUID("d7eb60b7-3cd3-41bc-b758-1f76d22e1748") : ["ACCESS"]}
    )  # Create a 2D array with None values

    organization2 = Organization(
        "Mert", "Organization 2", map ,{uuid.UUID("4629710e-d299-42da-a3e6-09f40b79e356") : ["LIST","ADD","ACCESS"], uuid.UUID("d7eb60b7-3cd3-41bc-b758-1f76d22e1748") : ["ACCESS"]}
    )  # Create a 2D array with None values

    organization3 = Organization(
        "Ece", "Organization 3", map ,{uuid.UUID("4629710e-d299-42da-a3e6-09f40b79e356") : ["LIST","ADD","ACCESS"], uuid.UUID("d7eb60b7-3cd3-41bc-b758-1f76d22e1748") : ["ACCESS"]}
    )  # Create a 2D array with None values
    
    eventList = [event1, event2, event3]
    organization.addRoom(room1)
    organization.addRoom(room2)
    organization.addRoom(room3)
    organization.addRoom(room4)

    organization.addEvent(event1)
    organization.addEvent(event2)
    organization.addEvent(event3)

    catalogue = Catalogue()
    catalogue.addOrganization(organization)
    organization.reserve(event1,room1,datetime(2022,2,1,9,0))
    organization.reserve(event2,room2,datetime(2022,3,1,9,0))
    #print(organization.query("Event","category",(0,0,5,5),None))
    print(organization.getEventsByRooms())
    

