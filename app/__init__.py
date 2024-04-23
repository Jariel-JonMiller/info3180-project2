from flask import Flask
from flask_login import LoginManager, UserMixin
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_bcrypt import Bcrypt
from flask_jwt_extended import JWTManager

from .config import Config

app = Flask(__name__)
app.config.from_object(Config)
app.config['JWT_SECRET_KEY'] = 'your_secret_key_here'


db = SQLAlchemy(app)
migrate = Migrate(app,db)
bcrypt = Bcrypt(app)
jwt = JWTManager(app)


login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'login'

from app import views