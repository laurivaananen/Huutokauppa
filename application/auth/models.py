from application import db
from application.models import Base

from sqlalchemy.sql import text

class UserAccount(Base):

    __tablename__ = "user_account"

    user_name = db.Column(db.String(144), nullable=False)
    first_name = db.Column(db.String(144), nullable=False)
    last_name = db.Column(db.String(144), nullable=False)

    #account_informations = db.relationship("account_information", backref='user_account', lazy=True)

    account_information_id = db.Column(db.Integer, db.ForeignKey('account_information.id'), nullable=False)

    def __init__(self,user_name, first_name, last_name, account_information):
        self.user_name = user_name
        self.first_name = first_name
        self.last_name = last_name
        self.account_information_id = account_information

    def get_id(self):
        return self.id

    def is_active(self):
        return True

    def id_anonymous(self):
        return False
    
    def is_authenticated(self):
        return True

class AccountInformation(Base):

    __tablename__ = "account_information"

    email_address = db.Column(db.String(144), nullable=False)
    password = db.Column(db.String(144), nullable=False)
    phone_number = db.Column(db.String(144), nullable=False)
    account_balance = db.Column(db.Integer(), nullable=False)
    banned = db.Column(db.Boolean(), nullable=False)

    user_account = db.relationship("UserAccount", backref='account_information', lazy=True, uselist=False)


    country_id = db.Column(db.Integer, db.ForeignKey('country.id'), nullable=False)
    city_id = db.Column(db.Integer, db.ForeignKey('city.id'), nullable=False)
    postal_code_id = db.Column(db.Integer, db.ForeignKey('postal_code.id'), nullable=False)
    street_address_id = db.Column(db.Integer, db.ForeignKey('street_address.id'), nullable=False)

    items = db.relationship('Item', backref='account_information', lazy=True)
    bids = db.relationship('Bid', backref='account_information', lazy=True)

    def __init__(self, email_address, password, phone_number, country, city, postal_code, street_address):
        self.email_address = email_address
        self.password = password
        self.phone_number = phone_number
        self.account_balance = 0
        self.banned = False

        self.country_id = country
        self.city_id = city
        self.postal_code_id = postal_code
        self.street_address_id = street_address


    def get_id(self):
        return self.id

    def is_active(self):
        return True

    def id_anonymous(self):
        return False
    
    def is_authenticated(self):
        return True


    @staticmethod
    def items_count(user_id=1):
        stmt = text("SELECT COUNT(item.id) AS item_count FROM item"
                    " INNER JOIN account_information ON account_information.id = item.account_information_id"
                    " WHERE account_information.id = :user_id;").params(user_id=user_id)
        res = db.engine.execute(stmt)

        result = res.fetchone()

        return result["item_count"]

    @staticmethod
    def bids_count(user_id=1):
        stmt = text("SELECT COUNT(bid.id) AS bid_count FROM bid"
                    " INNER JOIN account_information ON account_information.id = bid.account_information_id"
                    " WHERE account_information.id = :user_id;").params(user_id=user_id)
        res = db.engine.execute(stmt)

        result = res.fetchone()

        return result["bid_count"]

    @staticmethod
    def top_sellers():
        stmt = text("SELECT user_account.id AS user_id, user_account.user_name AS user_name, COUNT(item.id) AS item_count FROM account_information"
                    " LEFT JOIN item ON item.account_information_id = account_information.id"
                    " INNER JOIN user_account on user_account.account_information_id = account_information.id"
                    " WHERE item.sold = 1"
                    " GROUP BY user_account.id"
                    " ORDER BY item_count DESC;")

        res = db.engine.execute(stmt)
        
        response = []
        for row in res:
            response.append({"user_id":row[0], "user_name":row[1], "item_count":row[2]})

        return response


    @staticmethod
    def top_bidders():
        stmt = text("SELECT user_account.id AS user_id, user_account.user_name AS user_name, COUNT(bid.id) AS bid_count FROM account_information"
                    " INNER JOIN bid ON bid.account_information_id = account_information.id"
                    " INNER JOIN user_account on user_account.account_information_id = account_information.id"
                    " GROUP BY user_account.id"
                    " ORDER BY bid_count DESC;")

        res = db.engine.execute(stmt)
        
        response = []
        for row in res:
            response.append({"user_id":row[0], "user_name":row[1], "bid_count":row[2]})

        return response

class Country(Base):

    __tablename__ = "country"


    name = db.Column(db.String(144), nullable=False)



    account_informations = db.relationship("AccountInformation", backref='country', lazy=True)

    def __init__(self, name):
        self.name = name


class City(Base):

    __tablename__ = "city"


    name = db.Column(db.String(144), nullable=False)

    account_informations = db.relationship("AccountInformation", backref='city', lazy=True)
    # business_acounts = db.relationship("BusinessAccount", backref='city', lazy=True)

    def __init__(self, name):
        self.name = name

class PostalCode(Base):

    __tablename__ = "postal_code"


    name = db.Column(db.String(144), nullable=False)

    account_informations = db.relationship("AccountInformation", backref='postal_code', lazy=True)
    # business_acounts = db.relationship("BusinessAccount", backref='postal_code', lazy=True)

    def __init__(self, name):
        self.name = name

class StreetAddress(Base):

    __tablename__ = "street_address"


    name = db.Column(db.String(144), nullable=False)

    account_informations = db.relationship("AccountInformation", backref='street_address', lazy=True)
    # business_acounts = db.relationship("BusinessAccount", backref='street_address', lazy=True)

    def __init__(self, name):
        self.name = name