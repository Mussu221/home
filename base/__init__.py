import os
from flask import Flask
from base.database.db import initialize_db
from flask_login import LoginManager
from dotenv import load_dotenv
from base.api.user.auth import UPLOAD_FOLDER
from base.api.user.create import PROPERTY_FOLDER
load_dotenv()

def create_app():
    
    app = Flask(__name__)
    app.config['SECRET_KEY'] = os.getenv("SECRET_KEY")
    app.config['UPLOAD_FOLDER']=UPLOAD_FOLDER
    app.config['PROPERTY_FOLDER']=PROPERTY_FOLDER

    initialize_db(app)


    from base.api.user.auth import user_auth
    from base.api.user.create import user_create
    from base.api.user.view import user_view

    app.register_blueprint(user_auth)
    app.register_blueprint(user_create)
    app.register_blueprint(user_view)


    return app