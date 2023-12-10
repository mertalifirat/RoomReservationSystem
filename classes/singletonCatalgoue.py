class Singleton(object):
    
    def __new__(cls):
        if not hasattr(cls,'_inst'):
            cls._inst = super(Singleton,cls).__new__(cls)
        return cls._inst

class Catalogue(Singleton):
    
    def __init__(self):
        self.objectList = {}
        if not hasattr(self,'objectCount'):
            self.objectCount = 0

    def getCount(self):
        return self.objectCount
    
    def getObjectList(self):
        return self.objectList
    
    def add(self,object):
        self.objectList[object.getId()] = object
        self.objectCount += 1

    def get(self,id):
        return self.objectList[id]
