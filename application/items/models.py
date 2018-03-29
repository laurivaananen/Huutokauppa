from application import db

class Item(db.Model):
    id = db.Column(db.Integer, primary_key = True)
    date_created = db.Column(db.DateTime, default=db.func.current_timestamp())
    date_modified = db.Column(db.DateTime, default=db.func.current_timestamp(),
    onupdate=db.func.current_timestamp())

    starting_price = db.Column(db.Integer, nullable=False)
    buyout_price = db.Column(db.Integer, nullable=False)
    name = db.Column(db.String(256), nullable=False)
    sold = db.Column(db.Boolean, nullable=False)

    account_id = db.Column(db.Integer, db.ForeignKey('account.id'),
                           nullable=False)

    def __init__(self, name, buyout_price, starting_price, account_id):
        self.name = name
        self.buyout_price = buyout_price
        self.starting_price = starting_price
        self.sold = False
        self.account_id = account_id