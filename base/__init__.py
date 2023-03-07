import os
from flask import Flask
from base.database.db import initialize_db
from flask_login import LoginManager
from dotenv import load_dotenv
import stripe


load_dotenv()

login_manager = LoginManager()
 
login_manager.login_view='login'
login_manager.login_message_category='info'


stripe.api_key = 'rk_test_51MedQAFCatXUefOh70jO1tvPRvxLq8jtLERcCFM0T44RDECnXSexr7b3eC0BKdd3mNe9EllVf0VyNGwLpLkxYYDn00NRIPPShw'




def create_app():
    
    from base.api.user.auth import UPLOAD_FOLDER
    from base.api.user.create import PROPERTY_FOLDER
    from base.admin.create import CATEGORY_FOLDER

    app = Flask(__name__)
    app.config['SECRET_KEY'] = os.getenv("SECRET_KEY")
    app.config['UPLOAD_FOLDER']=UPLOAD_FOLDER
    app.config['PROPERTY_FOLDER']=PROPERTY_FOLDER
    app.config['CATEGORY_FOLDER']=CATEGORY_FOLDER

    initialize_db(app)
    
    login_manager.init_app(app)
    



    from base.api.user.auth import user_auth
    from base.api.user.create import user_create
    from base.api.user.view import user_view
    from base.admin.auth import admin_auth
    from base.admin.create import admin_create
    from base.admin.view import admin_view

    app.register_blueprint(user_auth,prefix_url='/')
    app.register_blueprint(user_create,prefix_url='/')
    app.register_blueprint(user_view,prefix_url='/')
    app.register_blueprint(admin_view,prefix_url='/')
    app.register_blueprint(admin_create,prefix_url='/')
    app.register_blueprint(admin_auth,prefix_url='/')


    return app