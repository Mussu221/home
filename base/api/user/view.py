from flask import url_for ,redirect , Blueprint ,flash, request ,jsonify
from base.api.user.models import token_required , Property, Property_image, Review, Wishlist, Booking
from base.database.db import db
from datetime import datetime
from sqlalchemy import desc
from geopy.distance import great_circle

user_view = Blueprint('user_view', __name__)



@user_view.route('/property_detail',methods=["GET"])
@token_required
def property_detail(active_user):
        property_id = request.args.get('property_id')
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
                print(i.created_at)
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
            return jsonify({'status':0,'message':'user is blocked'}) 
    else :
        bookings = Booking.query.filter_by(user_id=active_user.id).all()
        booking_list = []

        for booking in bookings:
            booking_dict ={}
            property = Property.query.filter_by(id=booking.property_id).first()
            review = Review.query.filter_by(property_id=property.id,user_id=active_user.id).first()
            if review:
                booking_dict['rating'] = review.rating
            elif not review :
                booking_dict['rating'] = "No Review"
            if booking.status == "p" or booking.status == "c": 
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
        booking_detail["price"] = property.price_per_night * 2
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



@user_view.route('/nearest', methods=['GET'])
@token_required
def nearest(active_user):

    lat = float(request.args.get('lat'))
    lon = float(request.args.get('lon'))

    data = Property.query.filter(Property.user_id != active_user.id).all()
    sorted_data = sorted(data, key=lambda x: great_circle((lat, lon), (x.latitude, x.longitude)).miles)[:5]
    
    return jsonify([{
       "Property_data":item.as_dict(),
        'distance': great_circle((lat, lon), (item.latitude, item.longitude)).miles
    } for item in sorted_data])
