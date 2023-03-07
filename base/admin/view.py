
from flask import url_for, redirect,render_template , Blueprint, flash, request
from flask_login import current_user, login_required
from base.admin.queryset import (total_user_count, all_users, total_property_count, all_property, 
                                total_booking_count, all_booking)
from base.admin.models import Content,Category, Language
from base.api.user.models import Property, Property_image, Booking, Review, User
from sqlalchemy import desc
admin_view = Blueprint('admin_view', __name__)

@admin_view.route('/admin/home')
@login_required
def home():
    users = total_user_count()
    property = total_property_count()
    booking = total_booking_count()

    return render_template('index.html', users=users, property=property, booking=booking, 
                            title="Homepage", page_name='Dashboard', is_active='home')


@admin_view.route("/admin/total_users", methods=['GET', 'POST'])
@login_required
def total_users():
    if  current_user.is_anonymous:
        flash("first login to access this page","info")
        return redirect(url_for('admin_auth.login'))
    else:
        
        page = request.args.get('page', 1, type=int)
        users = all_users(page)
        
    return render_template('total_user.html', users=users, Title="Total Users", page=page, page_name='Total Users', 
                            is_active='total_users')


@admin_view.route("/admin/total_property", methods=['GET', 'POST'])
@login_required
def total_property():
    if  current_user.is_anonymous:
        flash("first login to access this page","info")
        return redirect(url_for('admin_auth.login'))
    else:
        
        page = request.args.get('page', 1, type=int)
        properties = all_property(page)
        
    return render_template('total_property.html', properties=properties, Title="Total Properties", page=page, 
                            page_name='Total Properties', is_active='total_property',eval=eval,list=list,)


@admin_view.route("/admin/total_booking", methods=['GET', 'POST'])
@login_required
def total_booking():
    if  current_user.is_anonymous:
        flash("first login to access this page","info")
        return redirect(url_for('admin_auth.login'))
    else:
        
        page = request.args.get('page', 1, type=int)
        bookings = all_booking(page)
        
    return render_template('total_booking.html', bookings=bookings, Title="Total Active Bookings", page=page, 
                            page_name='Total Active Bookings', is_active='total_booking')



@admin_view.route("/admin/display_terms", methods=['GET','POST'])
def display_terms():
    content = Content.query.filter_by(id=1).first()

    return render_template('display_terms.html', content=content)


@admin_view.route("/admin/display_privacy", methods=['GET','POST'])
def display_privacy():
    content =  Content.query.filter_by(id=2).first()

    return render_template('display_privacy.html', content=content)


@admin_view.route("/admin/display_cancellation", methods=['GET','POST'])
def display_cancellation():
    content =  Content.query.filter_by(id=3).first()

    return render_template('display_cancellation.html', content=content)


@admin_view.route("/admin/display_review_process", methods=['GET','POST'])
def display_review_process():
    content =  Content.query.filter_by(id=4).first()

    return render_template('display_review_process.html', content=content)


@admin_view.route("/admin/display_timeshare_rules", methods=['GET','POST'])
def display_timeshare_rules():
    content =  Content.query.filter_by(id=5).first()

    return render_template('display_timeshare_rules.html', content=content)


@admin_view.route("/category")
def category():
    categories = Category.query.all()
    return render_template('add_category.html',categories=categories,title="Category" ,page='category',page_name='Property Category')


@admin_view.route("/language")
def language():
    language = Language.query.all()
    return render_template('host_language.html',language=language,title="Languages" ,page='language',page_name='Languages')

@admin_view.route("/<int:property_id>/property_detail")
def property_detail(property_id):

    property = Property.query.get(property_id)
    images = Property_image.query.filter_by(property_id=property_id).all()
    review = Review.query.filter_by(property_id=property_id).all()
    
    star1 = 0 
    star2 = 0 
    star3 = 0 
    star4 = 0 
    star5 = 0 

    for i in review :
        if i.rating == 1:
            star1+=1
        elif i.rating == 2:
            star2+=1
        elif i.rating == 3:
            star3+=1
        elif i.rating == 4:
            star4+=1
        elif i.rating == 5:
            star5+=1

    ratings={}
    average={}

    ratings[1] = star1
    ratings[2] = star2
    ratings[3] = star3
    ratings[4] = star4
    ratings[5] = star5

    if star1>=1 : 
        star1_average = star1/len(review)*100
        average[1]=star1_average

    if star2 >=1 :
        star2_average = star2/len(review)*100
        average[2]=star2_average

    if star3 >=1 :
        star3_average = star3/len(review)*100
        average[3]=star3_average

    if star4 >=1 :
        star4_average = star4/len(review)*100
        average[4]=star4_average

    if star5 >=1 :
        star5_average = star5/len(review)*100
        average[5]=star5_average

    sum = 0
    rating_average = 0
    average_rate =0
    for i in review :
        sum += i.rating
        if sum != 0 :
            average_rate = round((sum/len(review)),2)

    rating_average = average_rate*20

    total_review = len(review)    
    
    return render_template('property_detail.html',property=property,reviews=review,average_rate=average_rate,total_review=total_review, rating_average=rating_average , average=average, images=images,eval=eval,list=list, title="Property Detail" , len=len,page='property_detail',page_name='Property Detail',ratings=ratings)



@admin_view.route("/<int:user_id>/user_detail")
def user_detail(user_id):
    user = User.query.get(user_id)
    properties = Property.query.filter_by(user_id=user_id).order_by(Property.created_at.desc()).limit(3)
    bookings = Booking.query.filter_by(user_id=user_id).order_by(Booking.created_at.desc()).limit(3)
    booking_length = len(Booking.query.filter_by(user_id=user_id).all())
    property_length = len(Property.query.filter_by(user_id=user_id).all())
    total_review_count = 0
    overall_reviews= 0
    star1 = 0 
    star2 = 0 
    star3 = 0 
    star4 = 0 
    star5 = 0 
    for i in properties:

        reviews = Review.query.filter_by(property_id=i.id).all()

        for j in reviews:
            if j.rating == 1:
                star1+=1
            elif j.rating == 2:
                star2+=1
            elif j.rating == 3:
                star3+=1
            elif j.rating == 4:
                star4+=1
            elif j.rating == 5:
                star5+=1
            total_review_count +=1
            overall_reviews+= j.rating
    average_review=0
    if overall_reviews :
        average_review = overall_reviews/total_review_count

    average={}

    ratings = {1:star1,1:star1,2:star2,3:star3,4:star4,5:star5}

    if star1>=1 : 
        star1_average = star1/total_review_count*100
        average[1]=star1_average

    if star2 >=1 :
        star2_average = star2/total_review_count*100
        average[2]=star2_average

    if star3 >=1 :
        star3_average = star3/total_review_count*100
        average[3]=star3_average

    if star4 >=1 :
        star4_average = star4/total_review_count*100
        average[4]=star4_average

    if star5 >=1 :
        star5_average = star5/total_review_count*100
        average[5]=star5_average

    rating_average = average_review*20

    return render_template('user_detail.html',property_length=property_length,ratings=ratings,booking_length=booking_length, bookings=bookings, properties=properties, average=average, user=user,rating_average=rating_average, total_review_count=total_review_count, average_review=average_review,len=len,title="User Detail", page='property_detail',page_name='User Detail')


@admin_view.route("/<int:user_id>/user_detail/properties")
def user_properties(user_id):
    properties = Property.query.filter_by(user_id=user_id).all()

    return render_template('user_properties.html',properties=properties)
