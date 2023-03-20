'''
This is our initialization file.
The purpose of this file is to import flask
This is installed via pip or pip3: install flask.
-- "pip3 install flask"
This SHOULD give us: Flask, Jinja2, and Werkzeug.
If it doesn't those may need to be installed separately.
'''
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
# Yes, capital "F" on the import, otherwise this fails.



def create_app():
    '''
        Need to research which parts of this are actually necessary and why.
        But, "F" in Flask once again needs to be capital.
    '''
    app = Flask(__name__)
    app.config['SECRET_KEY'] = '123'
    
    from .views import views
    app.register_blueprint(views, url_prefix="/")
    '''
    The "views" here matches the file name.
    The ".views" here matches the concept as an attribute (object's name.)
    This is the registration process that is talked-about in views.py.
    If we set the prefix to something other than "/", THEN we can make
    the system look into folders if we have lots of files to include.
    '''
    return app