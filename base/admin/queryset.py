from base.api.user.models import User
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



def save():
    db.session.commit()