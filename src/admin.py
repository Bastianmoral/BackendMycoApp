import os
from flask_admin import Admin
from models import db, User, CollabUser, Collaboration, AttributeDescription, Observation, Mushrooms, Commentary, Post 
from flask_admin.contrib.sqla import ModelView

def setup_admin(app):
    app.secret_key = os.environ.get('FLASK_APP_KEY', 'sample key')
    app.config['FLASK_ADMIN_SWATCH'] = 'cerulean'
    admin = Admin(app, name='4Geeks Admin', template_mode='bootstrap3')

    
    # Add your models here, for example this is how we add a the User model to the admin
    admin.add_view(ModelView(User, db.session))
    admin.add_view(ModelView(CollabUser, db.session))
    admin.add_view(ModelView(Collaboration, db.session))
    admin.add_view(ModelView(AttributeDescription, db.session))
    admin.add_view(ModelView(Observation, db.session))
    admin.add_view(ModelView(Mushrooms, db.session))
    admin.add_view(ModelView(Commentary, db.session))
    admin.add_view(ModelView(Post, db.session))


    # You can duplicate that line to add mew models
    # admin.add_view(ModelView(YourModelName, db.session))