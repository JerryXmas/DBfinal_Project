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
@app.route('/Operation/Grow')
def grow():
    account = accountHandler.getAccountDataBySessionId(
                request.cookies.get('sessionId'))
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
@app.route('/Operation/Harvest')
def harvest():
    account = accountHandler.getAccountDataBySessionId(
                request.cookies.get('sessionId'))
    harvestList = locationHandler.selectAllHarvest(account.accountId)
    data = {"title": "Harvest",
            "Operation": active,
            "hasLogIn": True,
            "userName": "Hello " + account.userName,
            "harvestList": harvestList,
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

#------------------------------------Sale--------------------------------------
@app.route('/Operation/Sale')
def sale():
    account = accountHandler.getAccountDataBySessionId(
                request.cookies.get('sessionId'))
    transportList = locationHandler.selectAllTransport(account.accountId)
    data = {"title": "Sale",
            "Operation": active,
            "hasLogIn": True,
            "userName": "Hello " + account.userName,
            "transportList": transportList,
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
