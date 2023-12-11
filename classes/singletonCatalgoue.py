class Singleton(object):
    
    def __new__(cls):
        if not hasattr(cls,'_inst'):
            cls._inst = super(Singleton,cls).__new__(cls)
        return cls._inst

class Catalogue(Singleton):
    
    def __init__(self):
        self.userList = {}
        self.organizationList = {}
        if not hasattr(self,'objectCount'):
            self.objectCount = 0

    def getCount(self):
        return self.objectCount
    
    def getUserList(self):
        return self.userList
    
    def getOrganizationList(self):
        return self.organizationList
    
    def addUser(self,user):
        self.userList[user.getId()] = user
        self.objectCount += 1

    def addOrganization(self,organization):
        self.organizationList[organization.getId()] = organization
        self.objectCount += 1    

    def getUser(self,id):
        return self.userList[id]
    
    def getOrganization(self,id):
        return self.organizationList[id]
