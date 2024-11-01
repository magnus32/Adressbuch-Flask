from app import db

class Contacts(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(255), nullable=False)
    phone = db.Column(db.String(20), nullable=False)
    email = db.Column(db.String(255), nullable=False)
    address = db.Column(db.Text, nullable=False)
    date = db.Column(db.DateTime, default=db.func.current_timestamp())