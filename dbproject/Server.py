import os

from flask import (Flask, render_template, url_for, Markup, request, redirect,
                   make_response)
                   
from AccountHander import AccountHander
from LocationHander import LocationHander
                   
app = Flask(__name__)

active = Markup("class='active'")
dbUrl = "db.db3"
accountHandler = AccountHander(dbUrl)
locationHandler = LocationHander(dbUrl)
#-----------------------------------HomePage-----------------------------------
@app.route('/')
def homePage():
    data = {"title": "Home",
            "Home": active,
            }
    account = accountHandler.getAccountDataBySessionId(
                request.cookies.get('sessionId'))
    if account:
        data["userName"] = "Hello " + account.userName
        data["hasLogIn"] = True
    return render_template("Index.html", **data)
    
#------------------------------------Log In Out--------------------------------
@app.route('/LogIn', methods=["GET", "POST"])
def logIn():
    if request.method == "GET":
        data = {"title": "LogIn",
                "LogIn": active,
                }
        return render_template("LogIn.html", **data)
    elif request.method == "POST":
        accountName = request.form["account"]
        password = request.form["password"]
        sessionId = request.form["account"]
        account = accountHandler.hasTheAccount(accountName, password)
        if account:
            sessionId = accountHandler.insertSession(account)
            resp = make_response(redirect(url_for('homePage')))
            resp.set_cookie('sessionId', sessionId)
            return resp
        else:
            data = {"title": "LogIn",
                    "LogIn": active,
                    "wrong": "Account or Password are wrong !!",
                    }
            return render_template("LogIn.html", **data)
            
@app.route('/LogOut')
def logOut():
    accountHandler.deleteSession(request.cookies.get('sessionId'))
    return redirect(url_for('homePage'))
    
#---------------------------------Register--------------------------------------
@app.route('/Register', methods=["GET", "POST"])
def register():
    if request.method == "GET":
        data = {"title": "Register",
                "Register": active,
                }
        return render_template("Register.html", **data)
    elif request.method == "POST":
        accountName = request.form["accountName"]
        password = request.form["password"]
        userName = request.form["userName"]
        phone = "%s" % request.form["phone"]
        address = request.form["address"]
        e_mail = request.form["e_mail"]
        account = accountHandler.insertAccount(accountName, 
                                               password, userName, 
                                               phone, address, e_mail)
        sessionId = accountHandler.insertSession(account)
        resp = make_response(redirect(url_for('homePage')))
        resp.set_cookie('sessionId', sessionId)
        return resp
        
#---------------------------------Location-------------------------------------
@app.route('/View/Location')
def location():
    account = accountHandler.getAccountDataBySessionId(
                request.cookies.get('sessionId'))
    locations = locationHandler.selectAllLocations(account.accountId)
    
    data = {"title": "Location",
            "View": active,
            "hasLogIn": True,
            "userName": "Hello " + account.userName,
            "locations": locations,
            }
    return render_template("Location.html", **data)

#####-----------------------------add------------------------------------------
@app.route('/View/Location/AddLocation', methods=["GET", "POST"])
def addLocation():
    account = accountHandler.getAccountDataBySessionId(
                request.cookies.get('sessionId'))
    if request.method == "GET":
        data = {"title": "AddLocation",
                "View": active,
                "hasLogIn": True,
                "userName": "Hello " + account.userName,
                }
        return render_template("AddLocation.html", **data)
    elif request.method == "POST":
        locationName = request.form['locationName']
        address = request.form['address']
        hectare = int(request.form['hectare'])
        locationHandler.insertLocation(locationName, address, hectare, account.accountId)
        return redirect(url_for('location'))
        
#####------------------------------update--------------------------------------
@app.route('/View/Location/UpdateLocation/<int:locationId>', methods=["GET", "POST"])
def updateLocation(locationId):
    account = accountHandler.getAccountDataBySessionId(
                request.cookies.get('sessionId'))
    locations = locationHandler.selectAllLocations(account.accountId)
    location = None
    for l in locations:
        if l.id == locationId:
            location = l
            
    if request.method == "GET":
        data = {"title": "UpdateLocation",
                "View": active,
                "hasLogIn": True,
                "userName": "Hello " + account.userName,
                "location": location,
                }
        return render_template("UpdateLocation.html", **data)
    elif request.method == "POST":
        locationHandler.updateLocation(locationId, "L_Name", request.form['locationName'])
        locationHandler.updateLocation(locationId, "Address", request.form['address'])
        locationHandler.updateLocation(locationId, "Hectare", int(request.form['hectare']))
        return redirect(url_for('location'))
    
#####--------------------------------delete------------------------------------
@app.route('/View/Location/DeleteLocation/<int:locationId>', methods=["GET", "POST"])
def deleteLocation(locationId):
    account = accountHandler.getAccountDataBySessionId(
                request.cookies.get('sessionId'))
    locations = locationHandler.selectAllLocations(account.accountId)
    location = None
    for l in locations:
        if l.id == locationId:
            location = l
            
    if request.method == "GET":
        data = {"title": "DeleteLocation",
                "View": active,
                "hasLogIn": True,
                "userName": "Hello " + account.userName,
                "location": location,
                }
        return render_template("DeleteLocation.html", **data)
    elif request.method == "POST":
        if request.form['choose'] == 'yes':
            locationHandler.deleteLocation(locationId)
        return redirect(url_for('location'))
        
#---------------------------------Grow-----------------------------------------
@app.route('/Operation/Grow', methods=["GET", "POST"])
def grow():
    account = accountHandler.getAccountDataBySessionId(
                request.cookies.get('sessionId'))
    if request.method == "GET":
        growList = locationHandler.selectAllGrow(account.accountId)
        data = {"title": "Grow",
                "Operation": active,
                "hasLogIn": True,
                "userName": "Hello " + account.userName,
                "growList": growList,
                "locationHandler": locationHandler,
                "accountId": account.accountId
                }
        return render_template("Grow.html", **data)
    elif request.method == "POST":
        sdate = request.form['sdate']
        ddate = request.form['ddate']
        growList = locationHandler.selectAllGrow(account.accountId, date=(sdate, ddate))
        data = {"title": "Grow",
                "Operation": active,
                "hasLogIn": True,
                "userName": "Hello " + account.userName,
                "growList": growList,
                "locationHandler": locationHandler,
                "accountId": account.accountId,
                "sdate": sdate,
                "ddate": ddate,
                }
        return render_template("Grow.html", **data)
    
#####------------------------------add------------------------------------------
@app.route('/Operation/Grow/AddGrow', methods=["GET", "POST"])
def addGrow():
    account = accountHandler.getAccountDataBySessionId(
                request.cookies.get('sessionId'))
    locations = locationHandler.selectAllLocations(account.accountId)
    FCList = locationHandler.selectAllFC()
    if request.method == "GET":
        data = {"title": "AddGrow",
            "Operation": active,
            "hasLogIn": True,
            "userName": "Hello " + account.userName,
            "locations": locations,
            "FCList": FCList,
            }
        return render_template("AddGrow.html", **data)
    elif request.method == "POST":
        locationId = int(request.form['locationId'])
        FC_Id = int(request.form['FC_Id'])
        date = request.form['date']
        hectare = int(request.form['hectare'])
        locationHandler.insertGrow(locationId, FC_Id, date, hectare)
        return redirect(url_for('grow'))
        
#----------------------------------Harvest-------------------------------------
@app.route('/Operation/Harvest', methods=["GET", "POST"])
def harvest():
    account = accountHandler.getAccountDataBySessionId(
                request.cookies.get('sessionId'))
    if request.method == "GET":
        harvestList = locationHandler.selectAllHarvest(account.accountId)
        sumData = locationHandler.sumHarvest(account.accountId)
        sumP_Cost = 0
        for s in sumData:
            sumP_Cost += s[2]
        data = {"title": "Harvest",
                "Operation": active,
                "hasLogIn": True,
                "userName": "Hello " + account.userName,
                "harvestList": harvestList,
                "sumData": sumData,
                "sumP_Cost": sumP_Cost,
                }
        return render_template("Harvest.html", **data)
    elif request.method == "POST":
        sdate = request.form['sdate']
        ddate = request.form['ddate']
        harvestList = locationHandler.selectAllHarvest(account.accountId,  date=(sdate, ddate))
        sumData = locationHandler.sumHarvest(account.accountId, date=(sdate, ddate))
        sumP_Cost = 0
        for s in sumData:
            sumP_Cost += s[2]
        data = {"title": "Harvest",
                "Operation": active,
                "hasLogIn": True,
                "userName": "Hello " + account.userName,
                "harvestList": harvestList,
                "sdate": sdate,
                "ddate": ddate,
                "sumData": sumData,
                "sumP_Cost": sumP_Cost,
                }
        return render_template("Harvest.html", **data)
    
#####--------------------------------add---------------------------------------
@app.route('/Operation/Harvest/AddHarvest', methods=["GET", "POST"])
def addHarvest():
    account = accountHandler.getAccountDataBySessionId(
                request.cookies.get('sessionId'))
    locations = locationHandler.selectAllLocations(account.accountId)
    FCList = locationHandler.selectAllFC()
    if request.method == "GET":
        data = {"title": "AddHarvest",
            "Operation": active,
            "hasLogIn": True,
            "userName": "Hello " + account.userName,
            "locations": locations,
            "FCList": FCList,
            }
        return render_template("AddHarvest.html", **data)
    elif request.method == "POST":
        locationId = int(request.form['locationId'])
        FC_Id = int(request.form['FC_Id'])
        date = request.form['date']
        catty = int(request.form['catty'])
        pack_cost = int(request.form['pack_cost'])
        locationHandler.insertHarvest(locationId, FC_Id, date, catty, pack_cost)
        return redirect(url_for('harvest'))

#####-------------------------------update--------------------------------------
@app.route('/Operation/Harvest/UpdateHarvest/<int:H_Id>', methods=["GET", "POST"])
def updateHarvest(H_Id):    
    account = accountHandler.getAccountDataBySessionId(
                request.cookies.get('sessionId'))
    if request.method == "GET":
        locations = locationHandler.selectAllLocations(account.accountId)
        FCList = locationHandler.selectAllFC()
        harvest = locationHandler.getHarvestById(account.accountId, H_Id)
        data = {"title": "UpdateHarvest",
                "Operation": active,
                "hasLogIn": True,
                "userName": "Hello " + account.userName,
                "harvest": harvest,
                "locations": locations,
                "FCList": FCList,
                }
        return render_template("UpdateHarvest.html", **data)
    elif request.method == "POST":
        locationId = int(request.form['locationId'])
        locationHandler.updateHarvest(H_Id, "L_Id", locationId)
        FC_Id = int(request.form['FC_Id'])
        locationHandler.updateHarvest(H_Id, "FC_Id", FC_Id)
        date = request.form['date']
        locationHandler.updateHarvest(H_Id, "Date", date)
        catty = int(request.form['catty'])
        locationHandler.updateHarvest(H_Id, "Catty", catty)
        pack_cost = int(request.form['pack_cost'])
        locationHandler.updateHarvest(H_Id, "Pack_Cost", pack_cost)
        return redirect(url_for('harvest')) 

#####---------------------------------delete-----------------------------------
@app.route('/Operation/Harvest/DeleteHarvest/<int:H_Id>', methods=["GET", "POST"])
def deleteHarvest(H_Id):
    account = accountHandler.getAccountDataBySessionId(
                request.cookies.get('sessionId'))
    if request.method == "GET":
        data = {"title": "DeleteHarvest",
                "Operation": active,
                "hasLogIn": True,
                "userName": "Hello " + account.userName,
                "H_Id": H_Id,
                }
        return render_template("DeleteHarvest.html", **data)
    elif request.method == "POST":
        if request.form['choose'] == 'yes':
            locationHandler.deleteHarvest(H_Id)
        return redirect(url_for('harvest'))        

#------------------------------------Sale--------------------------------------
@app.route('/Operation/Sale', methods=["GET", "POST"])
def sale():
    account = accountHandler.getAccountDataBySessionId(
                request.cookies.get('sessionId'))
    if request.method == "GET":
        transportList = locationHandler.selectAllTransport(account.accountId)
        sumData = locationHandler.sumTransport(account.accountId)
        sumIncome = 0
        sumCost = 0
        for s in sumData:
            sumIncome += s[2]
            sumCost += s[3]
        data = {"title": "Sale",
                "Operation": active,
                "hasLogIn": True,
                "userName": "Hello " + account.userName,
                "transportList": transportList,
                "sumData": sumData,
                "sumIncome": sumIncome,
                "sumCost": sumCost,
                }
        return render_template("Sale.html", **data) 
    elif request.method == "POST":
        sdate = request.form['sdate']
        ddate = request.form['ddate']
        transportList = locationHandler.selectAllTransport(account.accountId, date=(sdate, ddate))
        sumData = locationHandler.sumTransport(account.accountId, date=(sdate, ddate))
        sumIncome = 0
        sumCost = 0
        for s in sumData:
            sumIncome += s[2]
            sumCost += s[3]
        data = {"title": "Sale",
                "Operation": active,
                "hasLogIn": True,
                "userName": "Hello " + account.userName,
                "transportList": transportList,
                "sdate": sdate,
                "ddate": ddate,
                "sumData": sumData,
                "sumIncome": sumIncome,
                "sumCost": sumCost,
                }
        return render_template("Sale.html", **data)

#####---------------------------------add--------------------------------------
@app.route('/Operation/Sale/AddSale', methods=["GET", "POST"])
def addSale():
    account = accountHandler.getAccountDataBySessionId(
                request.cookies.get('sessionId'))
    FCList = locationHandler.selectAllFC()
    customerList = locationHandler.selectAllCustomer()
    if request.method == "GET":
        data = {"title": "AddSale",
            "Operation": active,
            "hasLogIn": True,
            "userName": "Hello " + account.userName,
            "FCList": FCList,
            "customerList": customerList,
            }
        return render_template("AddSale.html", **data)
    elif request.method == "POST":
        customerId = int(request.form['customerId'])
        FC_Id = int(request.form['FC_Id'])
        date = request.form['date']
        catty = int(request.form['catty'])
        income = int(request.form['income'])
        cost = int(request.form['cost'])
        locationHandler.insertTransport(account.accountId , FC_Id, customerId, date, catty, income, cost)
        return redirect(url_for('sale')) 
        
#####-------------------------------update--------------------------------------
@app.route('/Operation/Sale/UpdateSale/<int:T_Id>', methods=["GET", "POST"])
def updateSale(T_Id):    
    account = accountHandler.getAccountDataBySessionId(
                request.cookies.get('sessionId'))
    if request.method == "GET":
        customerList = locationHandler.selectAllCustomer()
        FCList = locationHandler.selectAllFC()
        sale = locationHandler.getTransportById(account.accountId, T_Id)
        data = {"title": "UpdateHarvest",
                "Operation": active,
                "hasLogIn": True,
                "userName": "Hello " + account.userName,
                "sale": sale,
                "FCList": FCList,
                "customerList": customerList,
                }
        return render_template("UpdateSale.html", **data)
    elif request.method == "POST":
        customerId = int(request.form['customerId'])
        locationHandler.updateTransport(T_Id, "C_Id", customerId)
        FC_Id = int(request.form['FC_Id'])
        locationHandler.updateTransport(T_Id, "FC_Id", FC_Id)
        date = request.form['date']
        locationHandler.updateTransport(T_Id, "Date", date)
        catty = int(request.form['catty'])
        locationHandler.updateTransport(T_Id, "Catty", catty)
        income = int(request.form['income'])
        locationHandler.updateTransport(T_Id, "Income", income)
        cost = int(request.form['cost'])
        locationHandler.updateTransport(T_Id, "Cost", cost)
        return redirect(url_for('sale'))

#####---------------------------------delete-----------------------------------
@app.route('/Operation/Sale/DeleteSale/<int:T_Id>', methods=["GET", "POST"])
def deleteSale(T_Id):
    account = accountHandler.getAccountDataBySessionId(
                request.cookies.get('sessionId'))
    if request.method == "GET":
        data = {"title": "DeleteSale",
                "Operation": active,
                "hasLogIn": True,
                "userName": "Hello " + account.userName,
                "T_Id": T_Id,
                }
        return render_template("DeleteSale.html", **data)
    elif request.method == "POST":
        if request.form['choose'] == 'yes':
            locationHandler.deleteTransport(T_Id)
        return redirect(url_for('sale'))                

#------------------------------------FC----------------------------------------
@app.route('/View/FruitCrop')
def fruitCrop():
    account = accountHandler.getAccountDataBySessionId(
                request.cookies.get('sessionId'))
    FCList = locationHandler.selectAllFC()
    
    data = {"title": "FruitCrop",
            "View": active,
            "hasLogIn": True,
            "userName": "Hello " + account.userName,
            "FCList": FCList,
            }
    return render_template("FruitCrop.html", **data) 

#####--------------------------------add---------------------------------------
@app.route('/View/FruitCrop/AddFruitCrop', methods=["GET", "POST"])
def addFC():    
    account = accountHandler.getAccountDataBySessionId(
                request.cookies.get('sessionId'))
    if request.method == "GET":
        data = {"title": "AddFruitCrop",
                "View": active,
                "hasLogIn": True,
                "userName": "Hello " + account.userName,
                }
        return render_template("AddFruitCrop.html", **data)
    elif request.method == "POST":
        fcName = request.form['fcName']
        season = request.form['season']
        growthDution = request.form['growthDution']
        locationHandler.insertFC(fcName, season, growthDution)
        return redirect(url_for('fruitCrop'))
        
#####-------------------------------update--------------------------------------
@app.route('/View/FruitCrop/UpdateFruitCrop/<int:FC_Id>', methods=["GET", "POST"])
def updateFC(FC_Id):    
    account = accountHandler.getAccountDataBySessionId(
                request.cookies.get('sessionId'))
    if request.method == "GET":
        fc = locationHandler.getFCById(FC_Id)
        data = {"title": "UpdateFruitCrop",
                "View": active,
                "hasLogIn": True,
                "userName": "Hello " + account.userName,
                "fc": fc,
                }
        return render_template("UpdateFruitCrop.html", **data)
    elif request.method == "POST":
        fcName = request.form['fcName']
        locationHandler.updateFC(FC_Id, "Name", fcName)
        season = request.form['season']
        locationHandler.updateFC(FC_Id, "Season", season)
        growthDution = request.form['growthDution']
        locationHandler.updateFC(FC_Id, "GrowthDrution", growthDution)
        return redirect(url_for('fruitCrop'))
        
#####---------------------------------delete-----------------------------------
@app.route('/View/FruitCrop/DeleteFruitCrop/<int:FC_Id>', methods=["GET", "POST"])
def deleteFC(FC_Id):
    account = accountHandler.getAccountDataBySessionId(
                request.cookies.get('sessionId'))
    if request.method == "GET":
        data = {"title": "DeleteFruitCrop",
                "View": active,
                "hasLogIn": True,
                "userName": "Hello " + account.userName,
                "FC_Id": FC_Id,
                }
        return render_template("DeleteFruitCrop.html", **data)
    elif request.method == "POST":
        if request.form['choose'] == 'yes':
            locationHandler.deleteFC(FC_Id)
        return redirect(url_for('fruitCrop'))
        
#------------------------------------Customer---------------------------------
@app.route('/View/Customer')
def customer():
    account = accountHandler.getAccountDataBySessionId(
                request.cookies.get('sessionId'))
    customerList = locationHandler.selectAllCustomer()
    
    data = {"title": "Customer",
            "View": active,
            "hasLogIn": True,
            "userName": "Hello " + account.userName,
            "customerList": customerList,
            }
    return render_template("Customer.html", **data) 
    
#####--------------------------------add---------------------------------------
@app.route('/View/Customer/AddCustomer', methods=["GET", "POST"])
def addCustomer():    
    account = accountHandler.getAccountDataBySessionId(
                request.cookies.get('sessionId'))
    if request.method == "GET":
        data = {"title": "AddCustomer",
                "View": active,
                "hasLogIn": True,
                "userName": "Hello " + account.userName,
                }
        return render_template("AddCustomer.html", **data)
    elif request.method == "POST":
        name = request.form['name']
        phone = request.form['phone']
        address = request.form['address']
        e_mail = request.form['e_mail']
        locationHandler.insertCustomer(name, phone, address, e_mail)
        return redirect(url_for('customer'))
        
#####-------------------------------update--------------------------------------
@app.route('/View/Customer/UpdateCustomer/<int:C_Id>', methods=["GET", "POST"])
def updateCustomer(C_Id):    
    account = accountHandler.getAccountDataBySessionId(
                request.cookies.get('sessionId'))
    if request.method == "GET":
        c = locationHandler.getCustomerById(C_Id)
        data = {"title": "UpdateCustomer",
                "View": active,
                "hasLogIn": True,
                "userName": "Hello " + account.userName,
                "c": c,
                }
        return render_template("UpdateCustomer.html", **data)
    elif request.method == "POST":
        name = request.form['name']
        locationHandler.updateCustomer(C_Id, "Name", name)
        phone = request.form['phone']
        locationHandler.updateCustomer(C_Id, "Phone", phone)
        address = request.form['address']
        locationHandler.updateCustomer(C_Id, "Address", address)
        e_mail = request.form['e_mail']
        locationHandler.updateCustomer(C_Id, "E_mail", e_mail)
        return redirect(url_for('customer'))
        
#####---------------------------------delete-----------------------------------
@app.route('/View/Customer/DeleteCustomer/<int:C_Id>', methods=["GET", "POST"])
def deleteCustomer(C_Id):
    account = accountHandler.getAccountDataBySessionId(
                request.cookies.get('sessionId'))
    if request.method == "GET":
        data = {"title": "DeleteCustomer",
                "View": active,
                "hasLogIn": True,
                "userName": "Hello " + account.userName,
                "C_Id": C_Id,
                }
        return render_template("DeleteCustomer.html", **data)
    elif request.method == "POST":
        if request.form['choose'] == 'yes':
            locationHandler.deleteCustomer(C_Id)
        return redirect(url_for('customer'))
    
#-------------------------------------MAIN-------------------------------------
if __name__ == '__main__':
    app.run(debug=True)
