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
        rooms = {}
        for query in self.queryList:
            # for all querys' organizations

            # if not demanding rect based query
            if query.room is not None:
                # if room is reserved
                if query.organization.getRoom(query.room.getId())[1] is not None:
                    # append to given room name key's value in dict
                    rooms[query.room.getName()] += query.organization.query(
                        query.title, query.category, rect=None, room=query.room
                    )
        return rooms

    # Assuming start and end are given for a specific date intervals
    # start : datetime.datetime
    # end : datetime.datetime
    def dayView(self, start, end):
        days = {}
        delta = timedelta(days=1)
        tempStart = start
        while tempStart <= end:
            days[tempStart.date()] = []

            for query in self.queryList:
                queryRes = query.organization.query(
                    query.title, query.category, rect=query.rect, room=query.room
                )
                for res in queryRes:
                    if res[2].date() == tempStart.date():
                        days[tempStart.date()].append(res)

            tempStart += delta
        return days
