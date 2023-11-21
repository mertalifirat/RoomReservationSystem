from collections import OrderedDict
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

    def dayView(self, start, end):
        pass
