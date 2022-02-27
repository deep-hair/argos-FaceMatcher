from flask import Flask, Response
from flask_login import LoginManager
from flask_bootstrap import Bootstrap


from config import Config
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate

#Main
app = Flask(__name__,static_url_path='',
            static_folder='static',
            template_folder='templates')
app.config.from_object(Config)

#Login
login = LoginManager(app)
login.login_view = 'login'

#Database
db = SQLAlchemy(app)
migrate = Migrate(app, db)

#Bootstrap
bootstrap = Bootstrap(app)


from app import routes, models