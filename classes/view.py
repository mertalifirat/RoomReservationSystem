from collections import OrderedDict
from organization import Organization
import uuid
class View:
    def __init__(self,owner):
        self.id = uuid.uuid4()
        self.owner = owner
        self.queryList = OrderedDict()
    def addQuery(self,organization,title, category, rect=None, room=None):
        qid = uuid.uuid4()
        self.queryList[qid] = [organization,title, category, rect, room]
    def delQuery(self,qid):
        self.queryList.pop(qid)
    def roomView(self,start,end):
        for query in self.queryList:
            query.organization.query(query.title,query.category,query.rect,query.room)
            
    def dayView(self,start,end):
        pass
