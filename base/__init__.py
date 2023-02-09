import os
from flask import Flask
from base.database.db import initialize_db
from flask_login import LoginManager
from dotenv import load_dotenv
from base.api.user.auth import UPLOAD_FOLDER
from base.api.user.create import PROPERTY_FOLDER
load_dotenv()

login_manager = LoginManager()
 
login_manager.login_view='login'
login_manager.login_message_category='info'


def create_app():
    
    app = Flask(__name__)
    app.config['SECRET_KEY'] = os.getenv("SECRET_KEY")
    app.config['UPLOAD_FOLDER']=UPLOAD_FOLDER
    app.config['PROPERTY_FOLDER']=PROPERTY_FOLDER

    initialize_db(app)
    
    login_manager.init_app(app)


    from base.api.user.auth import user_auth
    from base.api.user.create import user_create
    from base.api.user.view import user_view
    from base.admin.auth import admin_auth
    from base.admin.view import admin_view

    app.register_blueprint(user_auth,prefix_url='/')
    app.register_blueprint(user_create,prefix_url='/')
    app.register_blueprint(user_view,prefix_url='/')
    app.register_blueprint(admin_view,prefix_url='/')
    app.register_blueprint(admin_auth,prefix_url='/')


    return app