from flask import render_template , url_for , request , flash , redirect , Blueprint , jsonify
from base.api.user.models import token_required, Property, Property_image, Review, Wishlist, Booking
from base.database.db import db
from werkzeug.utils import secure_filename
import secrets
import os
from datetime import datetime
user_create = Blueprint('user_create', __name__)



PROPERTY_FOLDER = "base/static/property_images"


@user_create.route('/add_property',methods=["POST"])
@token_required
def add_property(active_user):
    
    if request.method=="POST":
        title = request.form.get('title')
        address = request.form.get('address')
        latitude = request.form.get('latitude')
        longitude = request.form.get('longitude')
        city = request.form.get('city')
        state = request.form.get('state')
        zipcode = request.form.get('zipcode')
        guest_space = request.form.get('guest_space')
        bedrooms = request.form.get('bedrooms')
        beds = request.form.get('beds')
        bathrooms = request.form.get('bathrooms')
        about_property = request.form.get('about_property')
        amenities = request.form.getlist('amenities')
        house_rules = request.form.getlist('house_rules')
        price_per_night = request.form.get('price_per_night')  

 
        property = Property(
            title=title,
            address = address,
            latitude=latitude,
            longitude=longitude,
            city=city,
            state=state,
            zipcode=zipcode,
            guest_space=guest_space,
            bedrooms=bedrooms,
            beds=beds,
            bathrooms=bathrooms,
            about_property=about_property,
            amenities=amenities,
            house_rules= house_rules,
            price_per_night=price_per_night,
            user_id = active_user.id,
            created_at = datetime.utcnow()
        )

        db.session.add(property)
        db.session.commit()
        image_list=[]

        if request.files:

            images = request.files.getlist('images')
            print(images)

            for image in images : 
                if image.filename != '' :
                    image_name = secure_filename(image.filename)
                    extension = os.path.splitext(image_name)[1]
                    x = secrets.token_hex(10)
                    picture_fn = x + extension
                    image.save(os.path.join(PROPERTY_FOLDER, picture_fn))
                    image = Property_image(property_id=property.id, picture_name=picture_fn, created_at=datetime.utcnow())
                    db.session.add(image)
                    db.session.commit()

            images = Property_image.query.filter_by(property_id=property.id).all()
            for i in images :
                image_list.append(i.as_dict())

    return jsonify({
                    'status': 1,
                    'message': 'Property Added Successfully', 
                    'data':{
                            'property_detail':property.as_dict(),
                            'images': image_list
                            }
                    })


@user_create.route('/edit_property',methods=["POST"])
@token_required
def edit_property(active_user):
    if request.method=="POST":
        if active_user.is_block == 1:
            return jsonify({'success':0, 'message':'User is Blocked'})

        else :
            property_id=request.args.get('property_id')

            property=Property.query.filter_by(id=property_id).first()

            property.title = request.form.get('title')
            property.address = request.form.get('address')
            property.city = request.form.get('city')
            property.state = request.form.get('state')
            property.zipcode = request.form.get('zipcode')
            property.guest_space = request.form.get('guest_space')
            property.bedrooms = request.form.get('bedrooms')
            property.beds = request.form.get('beds')
            property.bathrooms = request.form.get('bathrooms')
            property.about_property = request.form.get('about_property')
            property.amenities = request.form.getlist('amenities')
            property.house_rules = request.form.getlist('house_rules')
            property.price_per_night = request.form.get('price_per_night')
            

            # if request.files :
            #     images = request.files.getlist('images')

            #     for form_picture  in images :
            #         image_name = secure_filename(form_picture.filename)
            #         extension = os.path.splitext(image_name)[1]
            #         x = secrets.token_hex(10)
            #         picture_fn = x + extension
            #         print(picture_fn)
            #         form_picture.save(os.path.join(PROPERTY_FOLDER, picture_fn))

            db.session.commit()

            return jsonify({
                    'status': 1,
                    'message': 'Property Updated Successfully', 
                    'data':{
                            'property_detail':property.as_dict(),
                            # 'images': image_list
                            }
                    })    

        
@user_create.route('/delete_property',methods=["POST"])
@token_required
def delete_property(active_user):
    if request.method=="POST":
        if active_user.is_block == 1:
            return jsonify({'success':0, 'message':'User is Blocked'})

        else :
            property_id=request.args.get('property_id')
            property=Property.query.filter_by(id=property_id).first()
            db.session.delete(property)
            db.session.commit()

            return jsonify({'status':1, 'message':'Property deleted successfully !'})


@user_create.route('/review',methods=["POST"])
@token_required
def review(active_user):
    if request.method=="POST":
        property_id = request.args.get('property_id')
        rating = request.form.get('rating')
        review = request.form.get('review')

        user_review=Review.query.filter_by(user_id=active_user.id , property_id=property_id).first()

        if active_user.is_block == 1:
            return jsonify({'success':0, 'message':'User is Blocked'})

        elif user_review:
            return jsonify({'status': 0, 'message':'Review is Already Given !'})

        else :
            new_review = Review(user_id=active_user.id, property_id=property_id, rating=rating, review=review, created_at = datetime.utcnow())
            db.session.add(new_review)
            db.session.commit()

            return jsonify({'status': 1, 'message':'Review added successfully',"data":new_review.as_dict()})


@user_create.route("/wishlist", methods=['GET', 'POST'])
@token_required
def add_wishlist(active_user):
    property_id = request.args.get('property_id')

    wishlist = Wishlist.query.filter_by(property_id=property_id,user_id=active_user.id).first()
    if active_user.is_block == 1:
            return jsonify({'success':0, 'message':'User is Blocked'})

    elif wishlist and wishlist.wishlist==True:
        wishlist.wishlist = False
        db.session.commit()
        return jsonify({'status': 0, 'message': 'Removed from wishlist',"data":wishlist.as_dict()})
    elif wishlist  and wishlist.wishlist==False : 
        wishlist.wishlist = True
        db.session.commit()
        return jsonify({'status': 1, 'message': 'Added to wishlist',"data":wishlist.as_dict()})
    elif not wishlist:
        wishlist = Wishlist(wishlist=True, property_id=property_id, user_id=active_user.id )
        db.session.add(wishlist)
        db.session.commit()
        return jsonify({'status': 0, 'message': 'Added to wishlist',"data":wishlist.as_dict()})


@user_create.route("/bookings", methods=["POST"])
@token_required
def create_booking(active_user):
    if request.method=="POST":
        if active_user.is_block == 1:
            return jsonify({'success':0, 'message':'User is Blocked'})
        else :
            property_id = request.args.get('property_id')
            start_date = request.form.get('start_date')
            end_date = request.form.get('end_date')
            guests = request.form.get('guests')
            cleaning_fees = request.form.get('cleaning_fees')
            discount = request.form.get('discount')
            service_fees = request.form.get('service_fees')
            total_charge = request.form.get('total_charge')
            description = request.form.get('description')

            booking = Booking(
                start_date=start_date,
                end_date=end_date,
                guests = guests,
                cleaning_fees=cleaning_fees,
                discount=discount,
                service_fees=service_fees,
                total_charge=total_charge,
                description=description,
                status="pending", 
                user_id = active_user.id,
                property_id = property_id
                )

            db.session.add(booking)
            db.session.commit()

            return jsonify({"status":1,"message":"Booking Successful.","data":booking.as_dict()})
