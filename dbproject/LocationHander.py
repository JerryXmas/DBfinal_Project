import sqlite3

from Location import Location
from FruitCrop import FruitCrop
from Grow import Grow

class LocationHander(object):
    def __init__(self, dataUrl):
        self.dbName = dataUrl
    
    def selectAllLocations(self, accountId):
        conn = sqlite3.connect(self.dbName)
        locationCursor = conn.cursor()
        data = locationCursor.execute(
                   "select * from Location where AccountId = %d" % accountId
               ).fetchall()
        locationCursor.close()
        
        locations = []
        
        for ldata in data:
            location = Location(ldata[0], ldata[1], ldata[2], ldata[3], ldata[4])
            growCursor = conn.cursor()
            growData = growCursor.execute(
                           "select * from Grow, FruitCrop where (Grow.FC_Id) = FruitCrop.Id and Grow.L_Id = %d" % ldata[0]
                       ).fetchall()
            for g in growData:
                FC = FruitCrop(g[4], g[5], g[6], g[7])
                grow = Grow(g[0], g[1], FC, g[2], g[3])
                location.appendGrow(grow)
            growCursor.close()
            locations.append(location)
        conn.close()
        return locations
        
    def insertLocation(self, locationName, address, hectare, accountId):
        conn = sqlite3.connect(self.dbName)
        locationCursor = conn.cursor()
        locationCursor.execute(
            "insert into Location values(Null, '%s', '%s', %d, %d);" % (locationName, address, hectare, accountId)
        )
        conn.commit()
        locationCursor.close()
        conn.close()
        
    def updateLocation(self, locationId, data, changeto):
        conn = sqlite3.connect(self.dbName)
        locationCursor = conn.cursor()
        if data == "Hectare":
            locationCursor.execute(
                "update Location set %s = %d where Id = %d;" % (data, changeto, locationId)
            )
        else:
            locationCursor.execute(
                "update Location set %s = '%s' where Id = %d;" % (data, changeto, locationId)
            )
        conn.commit()
        locationCursor.close()
        conn.close()
        
    def deleteLocation(self, locationId):
        conn = sqlite3.connect(self.dbName)
        locationCursor = conn.cursor()
        locationCursor.execute(
            "delete from Location where Id = %d;" % locationId
        )
        conn.commit()
        locationCursor.close()
        conn.close()
        
    def getLocationById(self, accountId, locationId):
        locations = self.selectAllLocations(accountId)
        location = None
        for l in locations:
            if l.id == locationId:
                location = l
        return location
        
    def selectAllGrow(self, accountId):
        conn = sqlite3.connect(self.dbName)
        growCursor = conn.cursor()
        growData = growCursor.execute(
                           ("select * from Grow, FruitCrop, Location, Account "
                            "where (Grow.FC_Id) = FruitCrop.Id and Grow.L_Id = Location.Id "
                            "and Location.AccountId = Account.Id and AccountId = %d order by Grow.Date DESC;") % accountId
                       ).fetchall()
        
        growList = []
        for g in growData:
            FC = FruitCrop(g[4], g[5], g[6], g[7])
            grow = Grow(g[0], g[1], FC, g[2], g[3])
            growList.append(grow)

        growCursor.close()
        conn.close()
        return growList
        
    def selectAllFC(self):
        conn = sqlite3.connect(self.dbName)
        FCCursor = conn.cursor()
        FCData = FCCursor.execute(
            "select * from FruitCrop"
        )
        FCList = []
        for fc in FCData:
            FC = FruitCrop(fc[0], fc[1], fc[2], fc[3])
            FCList.append(FC)
        FCCursor.close()
        conn.close()
        return FCList
        
    def insertGrow(self, locationId, FC_Id, date, hectare):
        conn = sqlite3.connect(self.dbName)
        growCursor = conn.cursor()
        growCursor.execute(
            "insert into Grow values(%d, %d, '%s', %d);" % (locationId, FC_Id, date, hectare)
        )
        
        conn.commit()
        growCursor.close()
        conn.close()
        