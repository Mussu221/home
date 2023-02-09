import jwt, os
from datetime import datetime, timedelta
from flask import redirect, render_template, request, flash, jsonify, url_for, Blueprint
from werkzeug.security import generate_password_hash
from base.database.db import db
from base.api.user.queryset import validate, insert_data, view_data
from dotenv import load_dotenv
from base.api.user.models import User , token_required
from base.api.user.utils import send_reset_email 
from werkzeug.utils import secure_filename
import secrets




UPLOAD_FOLDER = 'base/static/profile_pic/'


load_dotenv()

user_auth = Blueprint('user_auth', __name__)


@user_auth.route('/register', methods=['POST'])
def register():  
    if request.method == 'POST':

        fullname = request.form.get('fullname')
        phone_no = request.form.get('phone_no')
        country_code = request.form.get('country_code')
        password = request.form.get('password')
        email = request.form.get('email')
        device_id = request.form.get('device_id')
        device_type = request.form.get('device_type')
        hash_password = generate_password_hash(password)    
        image_name = 'default.png'

        user=validate(email)
        user_phone = User.query.filter_by(phone_no=phone_no).first()
        if fullname==None or phone_no==None or password==None or email==None or country_code==None or image_name==None :
            return jsonify({'status': 0, 'messege': 'Every field must have values'})

        elif user:
            return jsonify({'status': 0, 'messege': 'User Already Exits'})
        
        elif  user_phone:
            return jsonify(   {'status': 0, 'message': 'mobile number is already taken'})

        elif not user:
            user_data = User(fullname=fullname,country_code=country_code, email=email, device_id=device_id, device_type=device_type, phone_no=phone_no, password=hash_password,image_name=image_name, created_at=datetime.utcnow())
            insert_data(user_data)
            token = jwt.encode({'id': user_data.id, 'exp': datetime.utcnow() + timedelta(days = 365)},
                             os.getenv('SECRET_KEY'))
            # welcome_mail(user_data)
            return jsonify({'status': 1, 'message': 'success', 'data': user_data.as_dict(token)})


# otp_store ={}


# @user_auth.route('/verify_otp', methods=['GET'])
# def verify_otp():
#     user_phone = request.args.get('phone')
#     user_otp = request.args.get('otp')

#     # Check if the OTP entered by the user matches the one stored in the dictionary
#     if user_phone in otp_store and otp_store[user_phone] == user_otp:
#         return "OTP verified successfully!"
#     else:
#         return "Invalid OTP!"





@user_auth.route('/social_register', methods=['POST'])
def social_register():
    if request.method == 'POST':

        social_id = request.form.get('social_id')
        social_type = request.form.get('social_type')
        device_id = request.form.get('device_id')
        device_type = request.form.get('device_type')
        email = request.form.get('email')
        fullname = request.form.get('fullname')
        profile_pic = request.form.get('profile_pic')

        print(profile_pic, fullname, email)
        


        user = User.query.filter_by(social_id=social_id).first()

        if user:
            
            token = jwt.encode({'id': user.id, 'exp': datetime.utcnow() + timedelta(days = 365)}, os.getenv('SECRET_KEY'))
            return jsonify(
                {'status': 1, 'message': 'login successfully', 'data': user.as_dict(token) })

        if not user:

            user_data = User(social_id=social_id,
                                email= email,
                                fullname=fullname,
                                image_name=profile_pic,
                                social_type=social_type,
                                device_id=device_id,
                                device_type=device_type,
                                created_at=datetime.utcnow())

            insert_data(user_data)

            token = jwt.encode({'id': user_data.id, 'exp': datetime.utcnow() + timedelta(days = 365)}, os.getenv('SECRET_KEY'))

        return jsonify({'status': 1, 'message':'Register Successful','data': user_data.as_dict(token) })
          


@user_auth.route('/login', methods=['POST'])
def user_login():
    if request.method == 'POST':
        email = request.form.get('email')
        password = request.form.get('password')
        user = validate(email)
        if not user:
            return {'status': 0, 'message': 'User Not Exits'}
        if user and user.check_password(password) and user.is_block==0:

            token = jwt.encode({'id': user.id, 'exp': datetime.utcnow() + timedelta(days=365)}, os.getenv('SECRET_KEY'))
            return jsonify(
                {'status': 1, 'message': 'login successfully', 'data': user.as_dict(token)})
        elif user and user.is_block==1:

            return jsonify(
                {'status': 0, 'message': 'User is blocked'})
        else:
            return jsonify({'status': 0, 'message': 'Wrong Password'})


@user_auth.route("/getuser")
@token_required
def getuser(active_user):
    if active_user and active_user.is_block==0:
        return jsonify({'status': 1, 'data': active_user.user_data()})
    elif active_user and active_user.is_block==1:
            return jsonify(
                {'status': 0, 'message': 'User is blocked'})


@user_auth.route('/change_password', methods=['POST'])
@token_required
def change_password(active_user):
    old_pwd = request.form.get('oldPassword')
    new_pwd = request.form.get('newPassword')
    confirm_pwd = request.form.get('confirmPassword')

    if active_user and active_user.check_password(old_pwd) and active_user.is_block==0:

        if new_pwd == old_pwd :
            return jsonify({'status': 0, 'message': 'New password must be different from previous password !'})
        elif new_pwd == confirm_pwd:
            hash_password = generate_password_hash(new_pwd)
            active_user.password = hash_password
            db.session.commit()

            return jsonify({'status': 1, 'message': 'Password changed successfully !'})
        else:
            return jsonify({'status': 0, 'message': 'Password Does Not Match !'})
    elif active_user and active_user.is_block==1:
            return jsonify(
                {'status': 0, 'message': 'User is blocked'})
    else:
        return jsonify({'status': 0, 'message': 'Old password is wrong !'})


@user_auth.route('/user/reset_request', methods=['GET', 'POST'])
def user_reset_request():  
    if request.method == 'POST':

        user_email = request.form.get('email')
        user = validate(user_email)

        if not user:
            return jsonify({'status':0, 'message': 'User does not exist !'})
        
        elif user and user.is_block==1:
            return jsonify(
                {'status': 0, 'message': 'User is blocked'})

        elif user  and user.is_block==0:
            send_reset_email(user)
            return jsonify({'status': 1, 'message': 'Reset Link has been send to your gmail'})


@user_auth.route('/user/user_reset_password/<token>', methods=['GET', 'POST'])
def user_reset_token(token):
    return render_template('forget_password.html',token=token)


@user_auth.route('/reset_password/<token>', methods=['GET', 'POST'])
def reset_password(token):
    user = User.verify_token(token)

    if user is None:
        return 'Invalid or Expired Token'

    if user and request.method == 'POST':
        new_password = request.form.get('password')
        confirm_password = request.form.get('confirm_password')
        if new_password == confirm_password:
            hash_password = generate_password_hash(new_password)
            user.password = hash_password
            db.session.commit()
            return redirect(url_for("user_auth.success"))
        else:
            flash('Password  does not match , Try Again.. ','danger')
            return redirect(url_for('user_auth.user_reset_token', token=token))
    

@user_auth.route("/success", methods=['GET', 'POST'])
def success():
    return render_template('success_msg.html')


@user_auth.route('/user/update_profile', methods=['POST'])
@token_required
def user_update(active_user):
    user= validate(request.form.get("email"))

    if request.method == 'POST':

        if active_user and active_user.is_block==1:
            return jsonify({'status': 0, 'message': 'User is blocked'})

        elif  user and user.email!=active_user.email:
            return jsonify(   {'status': 0, 'message': 'email is already taken'})

        elif  user and user.phone!=active_user.phone:
            return jsonify(   {'status': 0, 'message': 'mobile number is already taken'})

        elif active_user and active_user.is_block==0:
                if request.files :
                    form_picture = request.files.get('image')
                    if active_user.image_name != 'default.png':
                        os.remove(os.path.join(UPLOAD_FOLDER,  active_user.image_name))
                    image_name = secure_filename(form_picture.filename)
                    extension = os.path.splitext(image_name)[1]
                    x = secrets.token_hex(10)
                    picture_fn = x + extension
                    print(picture_fn)
                    form_picture.save(os.path.join(UPLOAD_FOLDER, picture_fn))
                    active_user.image_name = picture_fn


                active_user.fullname = request.form.get('fullname')
                active_user.country_code = request.form.get('country_code')
                active_user.email = request.form.get('email')
                active_user.phone_no = request.form.get('phone_no')

                db.session.commit()

                return jsonify({'status': 1, 'message': 'Sucessfully Updated Profile', 'data': active_user.user_data()})
