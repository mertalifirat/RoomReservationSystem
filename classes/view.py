from collections import OrderedDict
from datetime import timedelta
from organization import Organization
import uuid


class View:
    def __init__(self, owner):
        self.id = uuid.uuid4()
        self.owner = owner
        self.queryList = OrderedDict()

    def addQuery(self, organization, title, category, rect=None, room=None):
        qid = uuid.uuid4()
        self.queryList[qid] = [organization, title, category, rect, room]

    def delQuery(self, qid):
        self.queryList.pop(qid)

    # start, end parameters are ignored due to pdf
    def roomView(self, start, end):
        queryRes = []
        rooms = {}
        #Getting results from all queries  
        for query in self.queryList:
            queryRes.extend(query.organization.query(
                query.title, query.category, rect=query.rect, room=query.room
            ))
        # Grouping (event,room,start) tuples by room and adding to the rooms dictionary    
        for event,room,start in queryRes:
            if room in rooms:
                rooms[room.getName()].append(event)
            else:
                rooms[room.getName()] = [event]    
        return rooms

    # Assuming start and end are given for a specific date intervals
    # start : datetime.datetime
    # end : datetime.datetime
    def dayView(self, start, end):
        queryRes = []
        days = {}
        #Getting results from all queries
        for query in self.queryList:
            queryRes.extend(query.organization.query(
                query.title, query.category, rect=query.rect, room=query.room
            ))
        # Grouping (event,room,start) tuples by day and adding to the days dictionary
        for res in queryRes:
            if res[2].date() not in days:
                days[res[2].date()].append(res)
            else:                   
                days[res[2].date()] = res
