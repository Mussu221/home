from flask import url_for ,redirect , Blueprint ,flash, request ,jsonify
from base.api.user.models import token_required , Property, Property_image


user_view = Blueprint('user_view', __name__)


@user_view.route('/property_detail',methods=["GET"])
@token_required
def property_detail(active_user):
    if request.method == "GET":
        property_id = request.args.get('property_id')
        property_detail = Property.query.filter_by(id=property_id).first()
        images = Property_image.query.filter_by(property_id=property_id).all()

        image_list=[]
        for i in images:

            image_list.append(i.as_dict())

        if active_user.is_block == 1:
            
            return jsonify({'status':0,"message":"user is  blocked !!"})
            
        else:

            return jsonify({"status":1,"message":"success","data":{"property_detail":property_detail.as_dict(), "images":image_list}})


@user_view.route('/my_property',methods=["GET"])
@token_required
def my_property(active_user):

        if active_user.is_block == 1 :
            return jsonify({'status':0,'message':'user is blocked'})
        
        else :
            my_properties =[]
            properties = Property.query.filter_by(user_id=active_user.id).all()
            property_dict ={}
            
            for i in properties:
                images = Property_image.query.filter_by(property_id=i.id).all()
                image_list=[]

                for j in images:
                    image_list.append(j.as_dict())

                property_dict['property_data']=i.as_dict()
                property_dict['images']=image_list
                my_properties.append(property_dict)


            return jsonify({'status':1, 'message':'my property', 'data':my_properties})

            


