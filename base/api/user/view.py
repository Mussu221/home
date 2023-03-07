from flask import url_for ,redirect , Blueprint ,flash, request ,jsonify
from base.api.user.models import token_required , Property, Property_image, Review, Wishlist, Booking, Visits
from base.admin.models import Category,Language
from base.database.db import db
from datetime import datetime
from sqlalchemy import desc
from geopy.distance import great_circle
from sklearn.neighbors import NearestNeighbors
import pandas as pd


user_view = Blueprint('user_view', __name__)


@user_view.route('/property_detail',methods=["GET"])
@token_required
def property_detail(active_user):

        property_id = request.args.get('property_id')
        visits = Visits.query.filter_by(user_id=active_user.id, property_id=property_id).first()

        if visits :
            visits.Visits += 1
            db.session.commit()

        else :
            visits = Visits(Visits=1,user_id=active_user.id, property_id=property_id, created_at=datetime.utcnow())
            db.session.add(visits)
            db.session.commit()

        property_detail = Property.query.filter_by(id=property_id).first()
        images = Property_image.query.filter_by(property_id=property_id).all()
        reviews = Review.query.filter_by(property_id=property_id).all()
        review_list = []

        for i in reviews:
            review_list.append(i.as_dict())
        image_list=[]
        for i in images:
            image_list.append(i.as_dict())
        if active_user.is_block == 1: 
            return jsonify({'status':0,"message":"user is  blocked !!"})
            
        else:
            return jsonify({"status":1,"message":"success","data":{"property_detail":property_detail.as_dict(), "images":image_list, "reviews":review_list}})


@user_view.route('/my_property',methods=["GET"])
@token_required
def my_property(active_user):
        properties = Property.query.filter_by(user_id=active_user.id).order_by(desc(Property.id)).all()
        if active_user.is_block == 1 :
            return jsonify({'status':0,'message':'user is blocked'}) 
        else :
            my_properties =[]   
            for i in properties:
                print(i.bookings)
                if i.bookings :
                    length  = len(i.bookings)
                    for j in i.bookings :
                        count = 0
                        if j.status=="completed":
                            count +=1
                        
                    
                    if length == count :
                        i.has_booking = False
                        db.session.commit()
                        
                property_dict ={}
                property_dict['property_data']=i.as_dict()
                images = Property_image.query.filter_by(property_id=i.id).order_by(desc(Property_image.created_at)).all()
                image_list=[]
                for j in images:
                    image_list.append(j.as_dict())             
                property_dict['images']=image_list
                my_properties.append(property_dict)
            
            return jsonify({'status':1, 'message':'my property', 'data':my_properties})

  

@user_view.route('/my_wishlist',methods=["GET"])
@token_required
def my_wishlist(active_user):
    if active_user.is_block == 1 :
            return jsonify({'status':0,'message':'user is blocked'}) 
    else :    
        wishlists = Wishlist.query.filter_by(user_id=active_user.id).all()
        wish_list =[]
        wishlist_dict = {}
        for wishlist in wishlists:
            property = Property.query.filter_by(id=wishlist.property_id).first()
            if wishlist.wishlist == True: 
               wishlist_dict['wishlist_data'] = wishlist.as_dict()
               wishlist_dict['property_data'] = property.as_dict()
        
        return jsonify({'status':1, 'message':'my property', 'data':wishlist_dict})


@user_view.route('/my_bookings',methods=["GET"])
@token_required
def my_bookings(active_user):
    if active_user.is_block == 1 :
            return jsonify({'status':0,'message':'User is blocked!'}) 
    else :
        bookings = Booking.query.filter_by(user_id=active_user.id).all()
        booking_list = []

        for booking in bookings:

            if datetime.utcnow() > booking.end_date :
                booking.status = "completed"
                db.session.commit()
            elif datetime.utcnow() < booking.start_date:
                booking.status = "upcoming"
                db.session.commit()
            elif datetime.utcnow() >= booking.start_date and datetime.utcnow() <= booking.end_date :
                booking.status = "active"
                db.session.commit()

            booking_dict ={}
            property = Property.query.filter_by(id=booking.property_id).first()
            review = Review.query.filter_by(property_id=property.id,user_id=active_user.id).first()
            if review:
                booking_dict['rating'] = review.rating
            elif not review :
                booking_dict['rating'] = "No Review"
            # if booking.status == "p" or booking.status == "c":
            booking_dict['address']= property.address
            booking_dict['amenities']= list(eval(property.amenities))
            booking_dict['status'] = booking.status
            booking_dict['price'] = property.price_per_night
            booking_list.append(booking_dict)

        return jsonify({'status':1, 'message':'my booking','data':booking_list})


@user_view.route('/booking_detail',methods=["GET"])
@token_required
def booking_detail(active_user):
    if active_user.is_block == 1 :
            
            return jsonify({'status':0,'message':'user is blocked'}) 
    else :

        booking_id = request.args.get('booking_id')
        booking = Booking.query.filter_by(id=booking_id,user_id=active_user.id).first()
        property = Property.query.filter_by(id=booking.property_id).first()
        booking_detail ={}
        booking_detail['guest'] = property.guest_space
        booking_detail["price"] = property.price_per_night 
        booking_detail['address'] = property.address
        booking_detail['amenities'] =  list(eval(property.amenities))
        booking_detail['end_date'] =  booking.end_date.strftime('%y-%m-%d')
        booking_detail['start_date'] =  booking.start_date.strftime('%y-%m-%d')
        booking_detail['discount'] = booking.discount
        booking_detail['cleaning_fees'] = booking.cleaning_fees
        booking_detail['service_fees'] = booking.service_fees
        booking_detail['total_price'] = booking.total_charge
        booking_detail['description'] =  booking.description

        return jsonify({'status':1, 'message':'my booking','data':booking_detail})



@user_view.route('/nearest', methods=['POST'])
@token_required
def nearest(active_user):

    lat = float(request.form.get('lat'))
    lon = float(request.form.get('lon'))

    data = Property.query.filter(Property.user_id != active_user.id).all()

    sorted_data = sorted(data, key=lambda x: great_circle((lat, lon), (x.latitude, x.longitude)).miles)[:5]
    nearby_list =[]
    for i in sorted_data:
        nearest_dict = {}

        nearest_dict['property_data'] = i.as_dict()
        images =Property_image.query.filter_by(property_id=i.id).all()
        image_list = []
        for j in images :
            image_list.append(j.as_dict())
        nearest_dict["images"]=image_list
        nearest_dict["distance"] = great_circle((lat, lon), (i.latitude, i.longitude)).miles
        nearby_list.append(nearest_dict)


    return jsonify({
       "status":1,"message":"recommendation","data": nearby_list
    })


@user_view.route('/recommendation', methods=['POST'])
@token_required
def recommendation(active_user):

    lat = float(request.form.get('lat'))
    lon = float(request.form.get('lon'))

    visits = Visits.query.filter_by(user_id=active_user.id).all()
    recommendation = []
    data = Property.query.filter(Property.user_id != active_user.id).all()
    sorted_data = sorted(data, key=lambda x: great_circle((lat, lon), (x.latitude, x.longitude)).miles)[:5]
    for i in sorted_data:
        recommend_dict = {}

        recommend_dict['property_data'] = i.as_dict()
        images =Property_image.query.filter_by(property_id=i.id).all()
        image_list = []
        for j in images :
            image_list.append(j.as_dict())
        print(image_list)  
        recommend_dict["images"]=image_list
        recommend_dict["distance"] = great_circle((lat, lon), (i.latitude, i.longitude)).miles
        recommendation.append(recommend_dict)

    for i in visits :
        property = Property.query.filter_by(id=i.property_id).first()
        recommendation.append(property.as_dict())
    
    for i  in sorted_data :
        if len(recommendation) < 5 and i.as_dict() not in recommendation:
            recommendation.append(i.as_dict())
        elif len(recommendation) > 5 :
            recommendation [0:5]


    return jsonify([{
       "Property_data":item
    } for item in recommendation])


@user_view.route('/filter', methods=['GET'])
@token_required
def filter(active_user):

    min_price = request.args.get('min_price', None, type=float)
    max_price = request.args.get('max_price', None, type=float)
    bedrooms = request.args.get('bedrooms', None, type=int)
    beds = request.args.get('beds', None, type=int)
    bathrooms = request.args.get('bathrooms', None, type=int)
    category_id = request.args.get('category_id', None, type=int)
    
    properties = Property.query

    if min_price:
        properties = properties.filter(Property.price_per_night >= min_price)

    if max_price:
        properties = properties.filter(Property.price_per_night <= max_price)
    
    if bedrooms:
        properties = properties.filter(Property.bedrooms == bedrooms)

    if beds:
        properties = properties.filter(Property.beds == beds)

    if bedrooms:
        properties = properties.filter(Property.bathrooms == bathrooms)
    
    if category_id:
        properties = properties.filter(Property.category_id == category_id)


    property = properties.all()
    property_list =[]
    for i in property :
        property_list.append(i.as_dict())

    
    return jsonify({"property_list":property_list})

@user_view.route("/get_category", methods=['GET'])
@token_required
def get_category(active_user):
    categories = Category.query.all()
    category_list = []
    for i in categories:
        category_list.append(i.as_dict())

    return jsonify({"status":1,'message':'Category List',"category_list":category_list})


@user_view.route("/get_language", methods=['GET'])
@token_required
def get_language(active_user):
    languages = Language.query.all()
    language_list = []
    for i in languages:
        language_list.append(i.as_dict())
        
    return jsonify({"status":1,'message':'Language List',"language_list":language_list})