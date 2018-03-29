from application import db

class User(db.Model):

    __tablename__ = "account"

    id = db.Column(db.Integer, primary_key=True)
    date_created = db.Column(db.DateTime, default=db.func.current_timestamp())
    date_modified = db.Column(db.DateTime, default=db.func.current_timestamp(),
                              onupdate=db.func.current_timestamp())

    first_name = db.Column(db.String(144), nullable=False)
    last_name = db.Column(db.String(144), nullable=False)
    email_address = db.Column(db.String(144), nullable=False)
    password = db.Column(db.String(144), nullable=False)

    items = db.relationship("Item", backref='account', lazy=True)

    def __init__(self, first_name, last_name, password, email_address):
        self.first_name = first_name
        self.last_name = last_name
        self.password = password
        self.email_address = email_address

    def get_id(self):
        return self.id

    def is_active(self):
        return True

    def id_anonymous(self):
        return False
    
    def is_authenticated(self):
        return True