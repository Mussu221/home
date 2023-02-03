from base.database.db import db
from base.api.user.models import User

def insert_data(x):
    db.session.add(x)
    db.session.commit()

def view_data():
    return User.query.all()

def  validate(x):
    return User.query.filter_by(email = x).first()
