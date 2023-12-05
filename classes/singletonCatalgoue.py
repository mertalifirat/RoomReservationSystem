class Singleton(object):
    
    def __new__(cls):
        if not hasattr(cls,'_inst'):
            cls._inst = super(Singleton,cls).__new__(cls)
        return cls._inst

class Catalogue(Singleton):
    objectList = {}
    def __init__(self):
        if not hasattr(self,'objectCount'):
            self.objectCount = 0

    def getCount(self):
        return self.objectCount
    
    def add(self,object):
        self.objectList[object.getId()] = object
        self.objectCount += 1

    def get(self,object):
        return self.objectList[object.getId()]
