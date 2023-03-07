from flask import render_template , url_for , request , flash , redirect , Blueprint , jsonify
from base.api.user.models import token_required, Property, Property_image, Review, Wishlist, Booking, User, PaymentInfo
from base.database.db import db
from werkzeug.utils import secure_filename
import secrets
import os
from datetime import datetime
from datetime import timedelta
# from base import stripe_keys
import stripe


user_create = Blueprint('user_create', __name__)



PROPERTY_FOLDER = "base/static/property_images"


@user_create.route('/add_property',methods=["POST"])
@token_required
def add_property(active_user):

    if not active_user.account  :
        account = stripe.Account.create(country="US",type="express",email = active_user.email, capabilities={"card_payments": {"requested": True}, "transfers": {"requested": True}})
        active_user.account=account.id
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
        category_id = request.form.get('category_id')
        type_of_property = request.form.get('type_of_property')
        type_of_place = request.form.get('type_of_place')
 
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
            has_booking = False,
            bathrooms=bathrooms,
            about_property=about_property,
            amenities=amenities,
            house_rules= house_rules,
            price_per_night=price_per_night,
            user_id = active_user.id,
            category_id = category_id,
            type_of_place=type_of_place,
            type_of_property=type_of_property,
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
            return jsonify({'status':0, 'message':'User is Blocked'})

        else :
            property_id=request.args.get('property_id')
            property = Property.query.get(property_id)

            if property.has_booking==True:
                return jsonify({'status':0, 'message':'Booking is active for this property ,so you can\'t edit this property . !'})
            

            else :

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
                property.property_id = request.form.get('property_id')
                property.price_per_night = request.form.get('price_per_night')
                property.type_of_place = request.form.get('type_of_place')
                property.type_of_property = request.form.get('type_of_property')
                property.category_id = request.form.get('category_id')
                db.session.commit()

                return jsonify({
                        'status': 1,
                        'message': 'Property Updated Successfully', 
                        'data':{
                                'property_detail':property.as_dict(),
                                # 'images': image_list
                                }
                        })    


# if request.files :
#     images = request.files.getlist('images')

#     for form_picture  in images :
#         image_name = secure_filename(form_picture.filename)
#         extension = os.path.splitext(image_name)[1]
#         x = secrets.token_hex(10)
#         picture_fn = x + extension
#         print(picture_fn)
#         form_picture.save(os.path.join(PROPERTY_FOLDER, picture_fn))

        
@user_create.route('/delete_property',methods=["POST"])
@token_required
def delete_property(active_user):
    if request.method=="POST":
        if active_user.is_block == 1:
            return jsonify({'status':0, 'message':'User is Blocked'})

        else :
            property_id=request.args.get('property_id')
            property = Property.query.get(property_id)

            if property.has_booking==True:
                return jsonify({'status':0, 'message':'Booking is active for this property ,so you can\'t delete this property . !'})
            
            else :
                property=Property.query.filter_by(id=property_id).first()
                image =Property_image.query.filter_by(property_id=property_id).all()
                for i in image :
                    os.remove(os.path.join(PROPERTY_FOLDER+'/'+i.picture_name))
                    db.session.delete(i)
                db.session.delete(property)
                db.session.commit()

                return jsonify({'status':1, 'message':'Property removed successfully.'})


@user_create.route('/review',methods=["POST"])
@token_required
def review(active_user):

    if request.method=="POST":
        booking_id = request.args.get('booking_id')
        rating = request.form.get('rating')
        review = request.form.get('review')

        booking = Booking.query.filter_by(user_id=active_user.id,id=booking_id).first()
        user_review=Review.query.filter_by(user_id=active_user.id ,booking_id=booking_id).first()
        review_time = booking.start_date + timedelta(days=2)  

        if active_user.is_block == 1:
            return jsonify({'status':0, 'message':'User is Blocked'})
            
        elif   datetime.utcnow() < booking.start_date or datetime.utcnow() > review_time:

                return jsonify({'status':0, 'message':'review can only be given between 48 hours from check-in time.'})

        elif user_review:

            if datetime.utcnow()  >= booking.start_date and datetime.utcnow() <= review_time:
                user_review.rating =rating
                user_review.review = review
                db.session.commit()
                return jsonify({'status': 1, 'message':'Review updated successfully',"data":user_review.as_dict()})

        else :
            
            new_review = Review(user_id=active_user.id, property_id=booking.property_id, rating=rating, review=review,booking_id=booking_id, created_at = datetime.utcnow())
            db.session.add(new_review)
            db.session.commit()
            return jsonify({'status': 1, 'message':'Review added successfully',"data":new_review.as_dict()})


@user_create.route('/get_review',methods=["GET"])
@token_required
def get_review(active_user):

    property_id = request.args.get('property_id')
    user_review=Review.query.filter_by(user_id=active_user.id , property_id=property_id).first()
    if user_review:
        return jsonify({'status': 1, 'message':'Review',"data":user_review.as_dict()})
    else :
        return jsonify({'status': 0, 'message':'No Review'})


@user_create.route("/wishlist", methods=['GET', 'POST'])
@token_required
def add_wishlist(active_user):

    property_id = request.args.get('property_id')

    wishlist = Wishlist.query.filter_by(property_id=property_id,user_id=active_user.id).first()
    
    if active_user.is_block == 1:
            return jsonify({'status':0, 'message':'User is Blocked'})

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

        property_id = request.args.get('property_id')
        property = Property.query.get(property_id)

        if active_user.is_block == 1:
            return jsonify({'stutus':0, 'message':'User is Blocked'})

        else :
            has_booking = False
            start_date = request.form.get('start_date')
            end_date = request.form.get('end_date')
            guests = request.form.get('guests')
            cleaning_fees = request.form.get('cleaning_fees')
            discount = request.form.get('discount')
            service_fees = request.form.get('service_fees')
            total_charge = request.form.get('total_charge')
            description = request.form.get('description')

            if property.has_booking == True :

                bookings = property.bookings

                for i in bookings:

                    booking_end = Booking.query.filter(Booking.end_date.between(start_date, end_date)).filter_by(property_id=i.property_id).first()
                    booking_start = Booking.query.filter(Booking.start_date.between(start_date, end_date)).filter_by(property_id=i.property_id).first()       
                    
                    if booking_start or booking_end:
                        has_booking = True
                        break

            if has_booking :

                return  jsonify({'stutus':0, 'message':'this property is already booked for these days , please select other day(s)!'})          

            
            elif has_booking == False or not property.has_booking :
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
                        property_id = property_id,
                        created_at = datetime.utcnow()
                        )
                    property.has_booking = True
                    db.session.add(booking)
                    db.session.commit()

                    return jsonify({"status":1,"message":"Booking Successful.","data":booking.as_dict()})


@user_create.route("/cancel_booking", methods=["POST"])
@token_required
def cancel_booking(active_user):

    if request.method == "POST":
        booking_id = request.args.get('booking_id')
        booking = Booking.query.filter_by(id=booking_id).first()
        if not booking :
                return jsonify({'stutus':0, 'message':'There is no booking.'})
        else :
            if booking.start_date <= datetime.utcnow():
                return jsonify({'stutus':0, 'message':'You can\'t cancel this booking.'})
            else:
                db.session.delete(booking)
                db.session.commit()
                return jsonify({'stutus':0, 'message':'Booking cancelled successfully.'})




@user_create.route('/verify_account', methods=['GET','POST'])
@token_required
def verify_account(active_user):

    account = stripe.Account.retrieve(active_user.account)
    if (account.charges_enabled == False and account.details_submitted == False and account.payouts_enabled == False and account.requirements.disabled_reason != None):
        create_link = stripe.AccountLink.create(account=account.id,refresh_url="https://example.com/reauth",return_url="https://example.com/return",type="account_onboarding",)
        
        return jsonify({'status': 1, 'data':create_link})


@user_create.route('/payment_intent', methods=['GET','POST'])
@token_required
def payment_intent(active_user):

        booking_id = request.args.get('booking_id')
        booking = Booking.query.get(booking_id)
        property = Property.query.get(booking.property_id)
        recipient  = User.query.get(property.user_id)
        customer = User.query.get(active_user.id)
        account = stripe.Account.retrieve(recipient.account)

        if not (account.charges_enabled == False and account.details_submitted == False and account.payouts_enabled == False and account.requirements.disabled_reason != None):
            recipient.account_verified = True
        db.session.commit()
        
        a = booking.total_charge

        payment_intent = stripe.PaymentIntent.create(
        amount = a,
        currency='usd',
        payment_method_types = ['card'],
        customer=active_user.customer_id,
        transfer_data = {
                        'destination':recipient.account,
                    },
        )
        payment_intent.save()

        property.status = 'upcoming'
        payment = PaymentInfo(customer=customer.id, recipient=recipient.id, booking_id = booking.id, customer_id=active_user.customer_id, recepient_acc_id=recipient.account ,
                                        intent_id=payment_intent.id, intent_secret=payment_intent.client_secret, amount=a)
        db.session.add(payment)
        db.session.commit()

        stripe.PaymentIntent.confirm(
        payment_intent.id,
        payment_method="pm_card_visa",
        )

        return jsonify({'stutus':0, 'message':'payment successful.','data':payment.as_dict()})