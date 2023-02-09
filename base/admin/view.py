
from flask import url_for ,redirect,render_template , Blueprint ,flash,request
from flask_login import current_user , login_required
from base.admin.queryset import (total_user_count,all_users)

admin_view = Blueprint('admin_view', __name__)

@admin_view.route('/admin/home')
@login_required
def home():
    users = total_user_count()
    return render_template('index.html',users=users,title="Home" ,page_name='Dashboard',is_active='home')


@admin_view.route("/total_users", methods=['GET', 'POST'])
@login_required
def total_users():
    if  current_user.is_anonymous:
        flash("first login to access this page","info")
        return redirect(url_for('admin_auth.login'))
    else :
        
        page = request.args.get('page', 1, type=int)
        users = all_users(page)
        
    return render_template('total_user.html',users=users,Title="Total Users",page=page, page_name='Total Users',is_active='total_users')
