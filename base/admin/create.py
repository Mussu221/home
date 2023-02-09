from flask import render_template , url_for , request , flash , redirect , Blueprint 
from base.admin.queryset import (delete_record,save,insert_data)

admin_create = Blueprint('admin_create', __name__)


