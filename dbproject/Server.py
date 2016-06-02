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
@app.route('/Location')
def location():
    account = accountHandler.getAccountDataBySessionId(
                request.cookies.get('sessionId'))
    locations = locationHandler.selectAllLocations(account.accountId)
    
    data = {"title": "Location",
            "Location": active,
            "hasLogIn": True,
            "userName": "Hello " + account.userName,
            "locations": locations,
            }
    return render_template("Location.html", **data)

#####-----------------------------add------------------------------------------
@app.route('/Location/AddLocation', methods=["GET", "POST"])
def addLocation():
    account = accountHandler.getAccountDataBySessionId(
                request.cookies.get('sessionId'))
    if request.method == "GET":
        data = {"title": "AddLocation",
                "Location": active,
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
@app.route('/Location/UpdateLocation/<int:locationId>', methods=["GET", "POST"])
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
                "Location": active,
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
@app.route('/Location/DeleteLocation/<int:locationId>', methods=["GET", "POST"])
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
                "Location": active,
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
    
    
#-------------------------------------MAIN-------------------------------------
if __name__ == '__main__':
    app.run(debug=True)
