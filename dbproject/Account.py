class Account(object):
    def __init__(self, accountId, accountName, password, userName, 
                 phone, address, e_mail):
        self.accountId = accountId
        self.accountName = accountName
        self.password = password
        self.userName = userName
        self.phone = phone
        self.address = address
        self.e_mail = e_mail