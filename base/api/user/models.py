import os,jwt
from functools import wraps
from flask import request,jsonify, url_for
from base.database.db import db
from werkzeug.security import  check_password_hash
from itsdangerous import TimedJSONWebSignatureSerializer as Serializer
import datetime
import enum 

class User(db.Model):
    id = db.Column('id', db.Integer, primary_key=True, autoincrement=True)
    fullname = db.Column('fullname', db.String(100))
    country_code = db.Column('country_code',db.String(100))
    phone_no = db.Column(db.String(15))
    email = db.Column('email', db.String(100))
    password = db.Column('password', db.String(200))
    image_name = db.Column('photo_name',db.String(100))
    is_block = db.Column(db.Boolean,default=False)
    device_id = db.Column('device_id', db.String(200))
    device_type = db.Column('device_type', db.String(50))
    social_id = db.Column('social_id', db.String(200))
    social_type = db.Column('social_type', db.String(50))
    created_at = db.Column(db.DateTime)
    updated_at = db.Column(db.DateTime, onupdate=datetime.datetime.utcnow())
    

    def check_password(self, password):
        return check_password_hash(self.password, password)

    def as_dict(self,token):
            return {
                    'id' : self.id,
                    'fullname' : self.fullname,
                    'email': self.email,
                    'country_code':self.country_code,
                    'phone_number':self.phone_no,
                    'profile_pic':self.image_name,
                    'social_id':self.social_id,
                    'social_type':self.social_type,
                    'device_id':self.device_id,
                    'device_type':self.device_type,
                    'token':{
                        'token': token
                    }
            }

    def user_data(self):
            return {
                    'id' : self.id,
                    'fullname' : self.fullname,
                    'email': self.email,
                    'country_code':self.country_code,
                    'phone_number':self.phone_no,
                    'profile_pic':self.image_name,
                    'social_id':self.social_id,
                    'social_type':self.social_type,
                    'device_id':self.device_id,
                    'device_type':self.device_type
            }

    def social_dict(self,token):
        return{
                'id':self.id,
                'social_id':self.social_id,
                'social_type':self.social_type,
                'device_id':self.device_id,
                'device_type':self.device_type,
                'token':{
                        'token': token
                    }
        }




    def get_token(self,expire_sec=1800):
        serial = Serializer(os.getenv("SECRET_KEY"),expire_sec)
        return serial.dumps({'user_id': self.id}).decode('utf-8')

    @staticmethod
    def verify_token(token):
        serial = Serializer(os.getenv('SECRET_KEY'))
        try:
            user_id = serial.loads(token)['user_id']
        except:
            return None
        return User.query.get(user_id)



def token_required(f):
    @wraps(f)
    def decorator(*args, **kwargs):
        token = None
        if 'authorization' in request.headers:
            token = request.headers['authorization']
        if not token:
            return jsonify({'status': 0,'message': 'a valid token is missing'})
        try:
            data = jwt.decode(token, os.getenv("SECRET_KEY"), algorithms=["HS256"])
            active_user = User.query.filter_by(id=data['id']).first()
        except:
            return jsonify({'status': 0,'message': 'token is invalid'})

        return f(active_user, *args, **kwargs)

    return decorator



class Property(db.Model):
    id = db.Column('id', db.Integer, primary_key=True, autoincrement=True)
    title = db.Column(db.String(100))
    address = db.Column(db.String(200))
    latitude = db.Column(db.String(200))
    longitude = db.Column(db.String(200))
    city = db.Column(db.String(200))
    state = db.Column(db.String(200))
    zipcode = db.Column(db.String(10))
    guest_space= db.Column(db.String(10))
    beds = db.Column(db.String(10))
    bathrooms = db.Column(db.String(10))
    bedrooms = db.Column(db.String(10))
    about_property = db.Column(db.Text)
    amenities = db.Column(db.String(200))
    house_rules = db.Column(db.String(200))
    price_per_night = db.Column(db.Integer)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id', ondelete='CASCADE', onupdate = 'CASCADE'))
    created_at = db.Column(db.DateTime)
    updated_at = db.Column(db.DateTime, onupdate=datetime.datetime.utcnow())
    ratings = db.relationship('Review', backref='ratings', lazy=True)


    def as_dict(self):

        reviews = Review.query.filter_by(property_id=self.id).all()
        sum = 0
        average = 0
        for i in reviews :
            sum += i.rating
        if sum != 0 :
            average = round((sum/len(reviews)),2)
            
        return{
                    'id' : self.id,
                    'title' : self.title,
                    'latitude': self.latitude,
                    'longitude': self.longitude,
                    'address': self.address,
                    'city':self.city,
                    'state':self.state,
                    'zipcode':self.zipcode,
                    'guest_space':self.guest_space,
                    'beds':self.beds,
                    'bedrooms':self.bedrooms,
                    'about_property':self.about_property,
                    'average_ratings':  average,
                    'amenities':list(eval(self.amenities)),
                    'house_rules':list(eval(self.house_rules)),
                    'price_per_night':self.price_per_night,
            }




class Property_image(db.Model):
    id = db.Column('id', db.Integer, primary_key=True, autoincrement=True)
    picture_name = db.Column(db.String(200))
    property_id = db.Column(db.Integer, db.ForeignKey('property.id', ondelete='CASCADE', onupdate = 'CASCADE'))
    created_at = db.Column(db.DateTime)
    updated_at = db.Column(db.DateTime, onupdate=datetime.datetime.utcnow())
    def as_dict(self):
        
        return{
            "id":self.id,
            "picture_name":self.picture_name,
            "property_id":self.property_id
        }


class Review(db.Model):
    id = db.Column('id', db.Integer, primary_key=True, autoincrement=True)
    rating = db.Column(db.Integer)
    review = db.Column(db.Text)
    property_id = db.Column(db.Integer, db.ForeignKey('property.id', ondelete='CASCADE', onupdate = 'CASCADE'))
    user_id = db.Column(db.Integer, db.ForeignKey('user.id', ondelete='CASCADE', onupdate = 'CASCADE'))
    created_at = db.Column(db.DateTime)
    updated_at = db.Column(db.DateTime, onupdate=datetime.datetime.utcnow())

    def as_dict(self):
        user = User.query.filter_by(id=self.user_id).first()
        return{
            "id":self.id,
            "rating":self.rating,
            "review":self.review,
            "property_id" : self.property_id,
            "create_date": self.created_at.strftime('%y-%m-%d'),
            "fullname": user.fullname
        }


class Wishlist(db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    wishlist = db .Column(db.Boolean)
    property_id = db.Column(db.Integer, db.ForeignKey('property.id', ondelete='CASCADE', onupdate = 'CASCADE'))
    user_id = db.Column(db.Integer, db.ForeignKey('user.id', ondelete='CASCADE', onupdate = 'CASCADE'))
    created_at = db.Column(db.DateTime)
    updated_at = db.Column(db.DateTime, onupdate=datetime.datetime.utcnow())

    def as_dict(self):

        return{
            "id":self.id,
            "wishlist":self.wishlist,
            "user_id":self.user_id,
            "property_id" : self.property_id,
        }

class Status(str,enum.Enum):
    pending       = 0  #pending payment 
    upcoming      = 1
    active        = 2
    completed     = 3


class Booking(db.Model):

    
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    start_date = db.Column(db.DateTime)
    guests = db.Column(db.String(100))
    end_date = db.Column(db.DateTime)
    cleaning_fees = db.Column(db.Integer)
    discount = db.Column(db.Integer)
    service_fees = db.Column(db.Integer)
    total_charge = db.Column(db.Integer)
    description = db.Column(db.Text)
    status = db.Column(db.Enum(Status))
    user_id = db.Column(db.Integer, db.ForeignKey('user.id', ondelete='CASCADE', onupdate = 'CASCADE'))
    property_id = db.Column(db.Integer, db.ForeignKey('property.id', ondelete='CASCADE', onupdate = 'CASCADE'))

    def as_dict(self):


        return{
            "id":self.id,
            "start_date":self.start_date,
            "end_date":self.end_date,
            "guest":self.guests,
            "cleaning_fees":self.cleaning_fees,
            "discount":self.discount,
            "service_fees":self.service_fees,
            "status":self.status,
            "total_charge":self.total_charge,
            "description":self.description,
            "user_id":self.user_id,
            "property_id" : self.property_id,
        }
