from application import db

class UserAccount(db.Model):

    __tablename__ = "UserAccount"

    id = db.Column(db.Integer, primary_key=True)
    date_created = db.Column(db.DateTime, default=db.func.current_timestamp())
    date_modified = db.Column(db.DateTime, default=db.func.current_timestamp(),
                              onupdate=db.func.current_timestamp())

    user_name = db.Column(db.String(144), nullable=False)
    first_name = db.Column(db.String(144), nullable=False)
    last_name = db.Column(db.String(144), nullable=False)

    #account_informations = db.relationship("AccountInformation", backref='UserAccount', lazy=True)

    account_informations = db.Column(db.Integer, db.ForeignKey('AccountInformation.id'), nullable=False)

    def __init__(self,user_name, first_name, last_name, account_information):
        self.user_name = user_name
        self.first_name = first_name
        self.last_name = last_name
        self.account_informations = account_information

    def get_id(self):
        return self.id

    def is_active(self):
        return True

    def id_anonymous(self):
        return False
    
    def is_authenticated(self):
        return True

class AccountInformation(db.Model):

    __tablename__ = "AccountInformation"

    id = db.Column(db.Integer, primary_key=True)
    date_created = db.Column(db.DateTime, default=db.func.current_timestamp())
    date_modified = db.Column(db.DateTime, default=db.func.current_timestamp(),
                              onupdate=db.func.current_timestamp())

    email_address = db.Column(db.String(144), nullable=False)
    password = db.Column(db.String(144), nullable=False)
    phone_number = db.Column(db.String(144), nullable=False)
    account_balance = db.Column(db.Integer(), nullable=False)
    banned = db.Column(db.Boolean(), nullable=False)

    #user_account = db.Column(db.Integer, db.ForeignKey('UserAccount.id'), nullable=False)

    user_accounts = db.relationship("UserAccount", backref='AccountInformation', lazy=True)


    country = db.Column(db.Integer, db.ForeignKey('Country.id'), nullable=False)
    city = db.Column(db.Integer, db.ForeignKey('City.id'), nullable=False)
    postal_code = db.Column(db.Integer, db.ForeignKey('PostalCode.id'), nullable=False)
    street_address = db.Column(db.Integer, db.ForeignKey('StreetAddress.id'), nullable=False)

    items = db.relationship('Item', backref='AccountInformation', lazy=True)

    def __init__(self, email_address, password, phone_number, country, city, postal_code, street_address):
        self.email_address = email_address
        self.password = password
        self.phone_number = phone_number
        self.account_balance = 0
        self.banned = False

        self.country = country
        self.city = city
        self.postal_code = postal_code
        self.street_address = street_address


    def get_id(self):
        return self.id

    def is_active(self):
        return True

    def id_anonymous(self):
        return False
    
    def is_authenticated(self):
        return True

class Country(db.Model):

    __tablename__ = "Country"

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(144), nullable=False)



    account_informations = db.relationship("AccountInformation", backref='Country', lazy=True)
    # business_acounts = db.relationship("BusinessAccount", backref='Country', lazy=True)

    def __init__(self, name):
        self.name = name


class City(db.Model):

    __tablename__ = "City"

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(144), nullable=False)

    account_informations = db.relationship("AccountInformation", backref='City', lazy=True)
    # business_acounts = db.relationship("BusinessAccount", backref='City', lazy=True)

    def __init__(self, name):
        self.name = name

class PostalCode(db.Model):

    __tablename__ = "PostalCode"

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(144), nullable=False)

    account_informations = db.relationship("AccountInformation", backref='PostalCode', lazy=True)
    # business_acounts = db.relationship("BusinessAccount", backref='PostalCode', lazy=True)

    def __init__(self, name):
        self.name = name

class StreetAddress(db.Model):

    __tablename__ = "StreetAddress"

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(144), nullable=False)

    account_informations = db.relationship("AccountInformation", backref='StreetAddress', lazy=True)
    # business_acounts = db.relationship("BusinessAccount", backref='StreetAddress', lazy=True)

    def __init__(self, name):
        self.name = name