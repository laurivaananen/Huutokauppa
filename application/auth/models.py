from application import db
from application.models import Base

class UserAccount(Base):

    __tablename__ = "UserAccount"

    user_name = db.Column(db.String(144), nullable=False)
    first_name = db.Column(db.String(144), nullable=False)
    last_name = db.Column(db.String(144), nullable=False)

    #account_informations = db.relationship("AccountInformation", backref='UserAccount', lazy=True)

    account_information = db.Column(db.Integer, db.ForeignKey('AccountInformation.id'), nullable=False)

    def __init__(self,user_name, first_name, last_name, account_information):
        self.user_name = user_name
        self.first_name = first_name
        self.last_name = last_name
        self.account_information = account_information

    def get_id(self):
        return self.id

    def is_active(self):
        return True

    def id_anonymous(self):
        return False
    
    def is_authenticated(self):
        return True

class AccountInformation(Base):

    __tablename__ = "AccountInformation"

    email_address = db.Column(db.String(144), nullable=False)
    password = db.Column(db.String(144), nullable=False)
    phone_number = db.Column(db.String(144), nullable=False)
    account_balance = db.Column(db.Integer(), nullable=False)
    banned = db.Column(db.Boolean(), nullable=False)

    user_account = db.relationship("UserAccount", backref='AccountInformation', lazy=True, uselist=False)


    country = db.Column(db.Integer, db.ForeignKey('Country.id'), nullable=False)
    city = db.Column(db.Integer, db.ForeignKey('City.id'), nullable=False)
    postal_code = db.Column(db.Integer, db.ForeignKey('PostalCode.id'), nullable=False)
    street_address = db.Column(db.Integer, db.ForeignKey('StreetAddress.id'), nullable=False)

    items = db.relationship('Item', backref='AccountInformation', lazy=True)
    bids = db.relationship('Bid', backref='AccountInformation', lazy=True)

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

class Country(Base):

    __tablename__ = "Country"


    name = db.Column(db.String(144), nullable=False)



    account_informations = db.relationship("AccountInformation", backref='Country', lazy=True)

    def __init__(self, name):
        self.name = name


class City(Base):

    __tablename__ = "City"


    name = db.Column(db.String(144), nullable=False)

    account_informations = db.relationship("AccountInformation", backref='City', lazy=True)
    # business_acounts = db.relationship("BusinessAccount", backref='City', lazy=True)

    def __init__(self, name):
        self.name = name

class PostalCode(Base):

    __tablename__ = "PostalCode"


    name = db.Column(db.String(144), nullable=False)

    account_informations = db.relationship("AccountInformation", backref='PostalCode', lazy=True)
    # business_acounts = db.relationship("BusinessAccount", backref='PostalCode', lazy=True)

    def __init__(self, name):
        self.name = name

class StreetAddress(Base):

    __tablename__ = "StreetAddress"


    name = db.Column(db.String(144), nullable=False)

    account_informations = db.relationship("AccountInformation", backref='StreetAddress', lazy=True)
    # business_acounts = db.relationship("BusinessAccount", backref='StreetAddress', lazy=True)

    def __init__(self, name):
        self.name = name