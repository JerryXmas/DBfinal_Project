import sqlite3
import random

from Account import Account

class AccountHander(object):
    def __init__(self, dataUrl):
        self.dbName = dataUrl
        
    def hasTheAccount(self, accountName, password):
        conn = sqlite3.connect(self.dbName)
        accountCursor = conn.cursor()
        data = accountCursor.execute(
                   ("select * from Account "
                    "where AccountName = ? and Password = ?"),
                   (accountName, password)
               ).fetchall()
               
        accountCursor.close()
        conn.close()
        
        if len(data) == 1:
            account = Account(data[0][0] , accountName, password, data[0][3], 
                              data[0][4], data[0][5], data[0][6])
            return account
        else:
            return None
        
    def insertSession(self, account):
        conn = sqlite3.connect(self.dbName)
        sessionCursor = conn.cursor()
        
        localtime = sessionCursor.execute(
                        "SELECT datetime('now', '30 minutes');"
                    ).fetchall()[0][0]
        sessionId = (random.choice('abcdefghijklmnopqrstuvwxyz') + 
                     str(random.randint(1, 99999)) +
                     random.choice('abcdefghijklmnopqrstuvwxyz'))   
        accountId = account.accountId
        sessionCursor.execute(
            "insert into Session values('%s', '%s', %d)" % 
            (sessionId, localtime, accountId)
        )
        conn.commit()
        sessionCursor.close()
        conn.close()
        return sessionId
    

    def getAccountDataBySessionId(self, sessionId):
        conn = sqlite3.connect(self.dbName)
        sessionCursor = conn.cursor()
        data = sessionCursor.execute(
                   ("select * from Session, Account "
                    "where Session.AccountId = Account.Id "
                    "and Session.Id = '%s'") % sessionId
               ).fetchall()
               
        sessionCursor.close()
        conn.close()
        
        if len(data) == 1:
            account = Account(data[0][3], data[0][4], data[0][5], data[0][6], 
                              data[0][7], data[0][8], data[0][9])
            return account
        return None
            
    def deleteExpiredSessions(self):
        conn = sqlite3.connect(self.dbName)
        sessionCursor = conn.cursor()
        localtime = sessionCursor.execute(
                        "SELECT datetime('now', 'localtime');").fetchall()[0][0]
        sessionCursor.execute(
            "delete from Session where ExpireDate > '%s'" % localtime)
            
        conn.commit()
        sessionCursor.close()
        conn.close()
        return
        
    def deleteSession(self, sessionId):
        conn = sqlite3.connect(self.dbName)
        sessionCursor = conn.cursor()
        sessionCursor.execute(
            "delete from Session where Id = '%s'" % sessionId)
            
        conn.commit()
        sessionCursor.close()
        conn.close()
        return

#----------------------------account crud---------------------------------------
    def insertAccount(self, accountName, password, userName, 
                      phone, address, e_mail):
        conn = sqlite3.connect(self.dbName)
        accountCursor = conn.cursor()
        print (accountName, password, userName, phone, address, e_mail)
        accountCursor.execute(
            "insert into Account values(Null, '%s', '%s', '%s', '%s', '%s', '%s');" % 
            (accountName, password, userName, phone, address, e_mail)
        )  
        conn.commit()
        accountCursor.close()
        conn.close()
        return self.hasTheAccount(accountName, password)
        
        