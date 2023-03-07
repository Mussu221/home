from flask import render_template , url_for , request , flash , redirect , Blueprint 
from base.admin.queryset import (delete_record,save,insert_data)
from flask_login import login_required
import os
from werkzeug.utils import secure_filename
import secrets
from base.admin.models import Category,Language
# from database.db import db
from PIL import Image
from datetime import datetime

CATEGORY_FOLDER = 'base/static/category_pic/'

admin_create = Blueprint('admin_create', __name__)


def crop_center(pil_img, crop_width, crop_height):
    img_width, img_height = pil_img.size
    return pil_img.crop(((img_width - crop_width) // 2,
                         (img_height - crop_height) // 2,
                         (img_width + crop_width) // 2,
                         (img_height + crop_height) // 2))

def crop_max_square(pil_img):

    return crop_center(pil_img, min(pil_img.size), min(pil_img.size))

@admin_create.route("/add_category",methods=['GET','POST'])
@login_required
def add_category():
    if request.method =="POST":
        cat_name = request.form.get('cat_name')
        cat_image=request.files['cat_image']
        print(cat_image)

        if cat_image.filename != '' :
            image_name = secure_filename(cat_image.filename)
            extension = os.path.splitext(image_name)[1]
            x = secrets.token_hex(10)
            picture_fn = x + extension

            image = Image.open(cat_image)
            image.resize((500,500))
            image_size = image.size 
            im_thumb = crop_center(image, image_size[0], image_size[0])
            im_thumb.save(os.path.join(CATEGORY_FOLDER, picture_fn), quality=100)

        category=Category(cat_name=cat_name,cat_image=picture_fn,created_at=datetime.utcnow())
        insert_data(category)

        flash('category updated successfully','success')
        return redirect(url_for('admin_view.category'))


@admin_create.route("/admin/<int:id>/edit_category",methods=['GET','POST'])
@login_required
def edit_category(id):
    if request.method=='POST':
        category =  Category.query.get(id)
        cat_image=request.files['profile_pic']
    
        if cat_image.filename != '' :
            os.remove(os.path.join(CATEGORY_FOLDER, category.cat_image))
            
            image_name = secure_filename(cat_image.filename)
            extension = os.path.splitext(image_name)[1]
            x = secrets.token_hex(10)
            picture_fn = x + extension
            image = Image.open(cat_image)
            image.resize((500,500))
            image_size = image.size 
            im_thumb = crop_center(image, image_size[0], image_size[0])
            im_thumb.save(os.path.join(CATEGORY_FOLDER, picture_fn), quality=100)
            category.cat_image = picture_fn

        category.cat_name = request.form.get('cat_name')
        
        save()
        flash('category updated successfully','success')
        return redirect(url_for('admin_view.category'))


@admin_create.route("/admin/<int:id>/delete",methods=['GET','POST'])
@login_required
def delete_category(id):
    if request.method=='POST':
        category =   Category.query.get(id)
        # os.remove(os.path.join(CATEGORY_FOLDER, category.cat_image))
        delete_record(category)
        flash('category Deleted successfully','success')
        return redirect(url_for('admin_view.category'))




@admin_create.route("/add_language",methods=['GET','POST'])
def add_language():
    if request.method=='POST':
        language = request.form.get('language')
        language=Language(language=language,created_at=datetime.utcnow())
        insert_data(language)
        flash('Language added successfully.','success')
        return redirect(url_for('admin_view.language'))


@admin_create.route("/admin/<int:id>/edit_language",methods=['GET','POST'])
def edit_language(id):
    if request.method=='POST':
        lang = Language.query.get(id)
        language=request.form.get('language')
        print(language)
        lang.language = language

        save()
        flash('Language updated successfully.','success')
        return redirect(url_for('admin_view.language'))


@admin_create.route("/admin/<int:id>/delete_language",methods=['GET','POST'])
def delete_language(id):
    if request.method=='POST':
        language = Language.query.get(id)
        delete_record(language)
        flash('Language Deleted successfully.','success')
        return redirect(url_for('admin_view.language'))


