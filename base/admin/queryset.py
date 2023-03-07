from base.api.user.models import User, Property, Booking
from base.admin.models import Admin
from base.database.db import db

def total_user_count():
    return len(User.query.all())

def insert_data(x):
    db.session.add(x)
    db.session.commit()

def all_users(page):
    return User.query.paginate(page=page, per_page=5)

def get_user(email):
    return Admin.query.filter_by(email=email).first()

def get_user_by_id(id):
    return Admin.query.filter_by(id=id).first()

def delete_record(x):
    db.session.delete(x)
    db.session.commit()

def total_property_count():
    return len(Property.query.all())

def all_property(page):
    return Property.query.paginate(page=page, per_page=5)

def total_booking_count():
    return len(Booking.query.filter_by(status='active').all())

def all_booking(page):
    return Booking.query.paginate(page=page, per_page=5)

def save():
    db.session.commit()
    