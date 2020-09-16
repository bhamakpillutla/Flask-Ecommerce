from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt


app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///myshop.db'
app.config['SECRET_KEY']="jasjqwewewsqi1212mwnqawj213"
db = SQLAlchemy(app)
bcrypt = Bcrypt(app)
 
 # registering the route
from shop.admin import routes