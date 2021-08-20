from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from datetime import datetime
import uuid

#Adding Flask Security for Passwords
from werkzeug.security import generate_password_hash, check_password_hash

#creates hex token for our API access
import secrets 

#imports login manager from flask_login package
from flask_login import LoginManager, UserMixin

#import for marshmallow marshaller
from flask_marshmallow import Marshmallow

db = SQLAlchemy()
login_manager = LoginManager()
ma = Marshmallow()

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(user_id)


class User(db.Model, UserMixin):
    id = db.Column(db.String, primary_key = True)
    email = db.Column(db.String(150), nullable = False, unique = True)
    password = db.Column(db.String, nullable = False)
    token = db.Column(db.String, unique = True)
    date_created = db.Column(db.DateTime, nullable = False, default = datetime.utcnow)
    recipe = db.relationship('Recipe', backref = 'owner', lazy = True)

    def __init__(self, email, password, token = '', id = ''):
        self.id = self.set_id()
        self.email = email
        self.password = self.set_password(password)
        self.token = self.set_token(24)

    def set_id(self):
        return str(uuid.uuid4())

    def set_password(self, password):
        self.pw_hash = generate_password_hash(password)
        return self.pw_hash

    def set_token(self, length):
        return secrets.token_hex(length)

class Recipe(db.Model):
    id = db.Column(db.String, primary_key = True)
    name = db.Column(db.String(150))
    description = db.Column(db.String(300))
    cook_time = db.Column(db.String(100))
    meat_or_veg = db.Column(db.String(50))
    garnishes = db.Column(db.String(300))
    spices = db.Column(db.String(300))
    user_token = db.Column(db.String, db.ForeignKey('user.token'), nullable = False)

    def __init__(self, name, description, cook_time, meat_or_veg, garnishes, spices, user_token, id = ''):
        self.id = self.set_id()
        self.name = name
        self.description = description
        self.cook_time = cook_time
        self.meat_or_veg = meat_or_veg
        self.garnishes = garnishes
        self.spices = spices
        self.user_token = user_token

    def set_id(self):
        return (secrets.token_urlsafe())


class RecipeSchema(ma.Schema):
    class Meta:
        fields = ['id', 'name', 'description', 'cook_time', 'meat_or_veg', 'garnishes', 'spices']


recipe_schema = RecipeSchema()
recipes_schema = RecipeSchema(many=True)