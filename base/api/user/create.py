from flask import render_template , url_for , request , flash , redirect , Blueprint , jsonify
from base.api.user.models import token_required, Property, Property_image, Review
from base.database.db import db
from werkzeug.utils import secure_filename
import secrets
import os
user_create = Blueprint('user_create', __name__)



PROPERTY_FOLDER = "base/static/property_images"


@user_create.route('/add_property',methods=["POST"])
@token_required
def add_property(active_user):

    if request.method=="POST":
        title = request.form.get('title')
        address = request.form.get('address')
        city = request.form.get('city')
        state = request.form.get('state')
        zipcode = request.form.get('zipcode')
        guest_space = request.form.get('guest_space')
        bedrooms = request.form.get('bedrooms')
        beds = request.form.get('beds')
        bathrooms = request.form.get('bathrooms')
        about_property = request.form.get('about_property')
        amenities = request.form.get('amenities')
        house_rules = request.form.get('house_rules')
        price_per_night = request.form.get('price_per_night')         
                
        property = Property(
            title=title,
            address=address,
            city=city,
            state=state,
            zipcode=zipcode,
            guest_space=guest_space,
            bedrooms=bedrooms,
            beds=beds,
            bathrooms=bathrooms,
            about_property=about_property,
            amenities=amenities,
            house_rules=house_rules,
            price_per_night=price_per_night,
            user_id = active_user.id,
        )
        db.session.add(property)
        db.session.commit()
        
        if request.files:
            images = request.files.getlist('images')

            for image in images : 
                image_name = secure_filename(image.filename)
                extension = os.path.splitext(image_name)[1]
                x = secrets.token_hex(10)
                picture_fn = x + extension
                print(picture_fn)
                image.save(os.path.join(PROPERTY_FOLDER, picture_fn))
                image = Property_image(property_id=property.id, picture_name=picture_fn)
                db.session.add(image)
                db.session.commit()

            images = Property_image.query.filter_by(property_id=property.id).all()
            image_list=[]
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
            property.amenities = request.form.get('amenities')
            property.house_rules = request.form.get('house_rules')
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

            return jsonify({'success':1, 'message':'Property deleted successfully !'})


@user_create.route('/review',methods=["POST"])
@token_required
def review(active_user):
    if request.method=="POST":
        property_id = request.args.get('property_id')
        rating = request.form.get('rating')
        review = request.form.get('review')

        review = Review(user_id=active_user.id, property_id=property_id, rating=rating, review=review)



        




        
        

    
