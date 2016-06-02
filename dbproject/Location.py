class Location(object):
    def __init__(self, id, name, address, hectare, accountId):
        self.id = id
        self.name = name
        self.address = address
        self.hectare = hectare
        self.accountId = accountId
        self.growList = []
        
    def appendGrow(self, grow):
        self.growList.append(grow)
        