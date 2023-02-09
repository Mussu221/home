from flask_login import UserMixin
from base.database.db import db
from datetime import datetime
from base import login_manager
from itsdangerous import TimedJSONWebSignatureSerializer as Serializer
import os 


       

@login_manager.user_loader
def load_user(user_id):
    return Admin.query.get(int(user_id))


class Admin(db.Model, UserMixin):
    id = db.Column(db.Integer,primary_key=True)
    fname=db.Column(db.String(150),nullable=True)
    lname=db.Column(db.String(150),nullable=True)
    email=db.Column(db.String(150),unique=True,nullable=True)
    phone=db.Column(db.String(150),nullable=True)
    image_file=db.Column(db.String(150),nullable=True)
    password = db.Column(db.String(150),nullable=True)
    created_at = db.Column(db.Date)
    updated_at = db.Column(db.DateTime, onupdate=datetime.utcnow())

    def get_reset_token(self,expiress_sec=1800):
        s=Serializer(os.getenv("SECRET_KEY"),expiress_sec)
        return s.dumps({'user_id':self.id}).decode('utf-8')

    @staticmethod
    def verify_reset_token(token):
        s=Serializer(os.getenv("SECRET_KEY"))
        try:
            user_id=s.loads(token)['user_id']
        except:
            return None
        return Admin.query.get(user_id)

class Terms(db.Model):
    id = db.Column(db.Integer,primary_key=True)
    content=db.Column(db.Text,nullable=True)
    created_at = db.Column(db.Date)
    updated_at = db.Column(db.DateTime, onupdate=datetime.utcnow())

    def as_dict(self):
        return{
            'id':self.id,
            'content':self.content
        }

class Privacy(db.Model):
    id = db.Column(db.Integer,primary_key=True)
    content=db.Column(db.Text,nullable=True)
    created_at = db.Column(db.Date)
    updated_at = db.Column(db.DateTime, onupdate=datetime.utcnow())

    def as_dict(self):
        return{
            'id':self.id,
            'content':self.content
        }
