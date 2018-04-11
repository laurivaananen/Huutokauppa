from application import db
from application.models import Base

class Bid(Base):

    __tablename__ = "Bid"

    amount = db.Column(db.Integer, nullable=False)

    account_information_id = db.Column(db.Integer, db.ForeignKey('AccountInformation.id'), nullable=False)

    item_id = db.Column(db.Integer, db.ForeignKey('Item.id'), nullable=False)

    def __init__ (self, amount, account_information_id, item_id):
        self.amount = amount
        self.account_information_id = account_information_id
        self.item_id = item_id

