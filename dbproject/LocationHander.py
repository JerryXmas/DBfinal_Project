import sqlite3

from Location import Location
from FruitCrop import FruitCrop
from Grow import Grow
from Harvest import Harvest
from Account import Account
from Transport import Transport
from Customer import Customer

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
        growCursor = conn.cursor()
        growCursor.execute(
            "delete from Grow where L_Id = %d" % locationId
        )
        conn.commit()
        growCursor.close()
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
        
    def selectAllHarvest(self, accountId):
        conn = sqlite3.connect(self.dbName)
        harvestCursor = conn.cursor()
        harvestData = harvestCursor.execute(
                           ("select * from Harvest, FruitCrop, Location, Account "
                            "where (Harvest.FC_Id) = FruitCrop.Id and Harvest.L_Id = Location.Id "
                            "and Location.AccountId = Account.Id and AccountId = %d order by Harvest.Date DESC;") % accountId
                       ).fetchall()
        harvestList = [] 
        for h in harvestData:
            location = self.getLocationById(h[15], h[1])
            FC = FruitCrop(h[6], h[7], h[8], h[9])
            harvest = Harvest(h[0], location, FC, h[3], h[4], h[5])
            harvestList.append(harvest)
            
        harvestCursor.close()
        conn.close()
        return harvestList
        
    def insertHarvest(self, locationId, FC_Id, date, catty, pack_cost):
        conn = sqlite3.connect(self.dbName)
        harvestCursor = conn.cursor()
        harvestCursor.execute(
            "insert into Harvest values(Null, %d, %d, '%s', %d, %d);" % (locationId, FC_Id, date, catty, pack_cost)
        )
        
        conn.commit()
        harvestCursor.close()
        conn.close()
        
    def selectAllTransport(self, accountId):
        conn = sqlite3.connect(self.dbName)
        transportCursor = conn.cursor()
        transportData = transportCursor.execute(
                            ("select * from Transport, FruitCrop, Account, Customer "
                             "where Transport.A_Id = Account.Id and Transport.FC_Id = FruitCrop.Id "
                             "and Transport.C_Id = Customer.Id and Transport.A_Id = %d") % accountId
                        ).fetchall()
        transportList = []
        for t in transportData:
            FC = FruitCrop(t[8], t[9], t[10], t[11])
            account = Account(t[12], t[13], t[14], t[15], t[16], t[17], t[18])
            customer = Customer(t[19], t[20], t[21], t[22], t[23])
            transport = Transport(t[0], account, FC, customer, t[4], t[5], t[6], t[7])
            transportList.append(transport)
        
        transportCursor.close()
        conn.close()
        return transportList
        
    def selectAllCustomer(self):
        conn = sqlite3.connect(self.dbName)
        customerCursor = conn.cursor()
        customerData = customerCursor.execute(
            "select * from Customer"
        )
        customerList = []
        for c in customerData:
            customer = Customer(c[0], c[1], c[2], c[3], c[4])
            customerList.append(customer)
        customerCursor.close()
        conn.close()
        return customerList
        
    def insertTransport(self, A_Id, FC_Id, C_Id, date, catty, income, cost):
        conn = sqlite3.connect(self.dbName)
        transportCursor = conn.cursor()
        transportCursor.execute(
            "insert into Transport values(Null, %d, %d, %d, '%s', %d, %d, %d);" % (A_Id, FC_Id, C_Id, date, catty, income, cost)
        )
        
        conn.commit()
        transportCursor.close()
        conn.close()
        
    def insertFC(self, fcName, season, growthDution):
        conn = sqlite3.connect(self.dbName)
        FCCursor = conn.cursor()
        FCCursor.execute(
            "insert into FruitCrop values(Null, '%s', '%s', '%s');" % (fcName, season, growthDution)
        )
        
        conn.commit()
        FCCursor.close()
        conn.close()
        
    def insertCustomer(self, name, phone, address, e_mail):
        conn = sqlite3.connect(self.dbName)
        customerCursor = conn.cursor()
        customerCursor.execute(
            "insert into Customer values(Null, '%s', '%s', '%s', '%s');" % (name, phone, address, e_mail)
        )
        
        conn.commit()
        customerCursor.close()
        conn.close()
        
    def getFCById(self, FC_Id):
        FCList = self.selectAllFC()
        for fc in FCList:
            if fc.FC_Id == FC_Id:
                return fc
                
    def getCustomerById(self, C_Id):
        customerList = self.selectAllCustomer()
        for c in customerList:
            if c.id == C_Id:
                return c
                
    def updateFC(self, FC_Id, data, changeto):
        conn = sqlite3.connect(self.dbName)
        FCCursor = conn.cursor()
        FCCursor.execute(
            "update FruitCrop set %s = '%s' where Id = %d;" % (data, changeto, FC_Id)
        )
        conn.commit()
        FCCursor.close()
        conn.close()
        
    def updateCustomer(self, C_Id, data, changeto):
        conn = sqlite3.connect(self.dbName)
        customerCursor = conn.cursor()
        customerCursor.execute(
            "update Customer set %s = '%s' where Id = %d;" % (data, changeto, C_Id)
        )
        conn.commit()
        customerCursor.close()
        conn.close()
     
    def deleteFC(self, FC_Id):
        conn = sqlite3.connect(self.dbName)
        FCCursor = conn.cursor()
        FCCursor.execute(
            "delete from FruitCrop where Id = %d;" % FC_Id
        )
        conn.commit()
        FCCursor.close()
        conn.close()
        
    def deleteCustomer(self, C_Id):
        conn = sqlite3.connect(self.dbName)
        customerCursor = conn.cursor()
        customerCursor.execute(
            "delete from Customer where Id = %d;" % C_Id
        )
        conn.commit()
        customerCursor.close()
        conn.close()
        
        