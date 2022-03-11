import torch
from flask import Flask
from flask_bootstrap import Bootstrap
from flask_login import LoginManager
from flask_migrate import Migrate
from flask_sqlalchemy import SQLAlchemy

from config import Config

#Main

app = Flask(__name__,static_url_path='',
            static_folder='static',
            template_folder='templates')
app.config.from_object(Config)

#Database
db = SQLAlchemy(app)
migrate = Migrate(app, db)

#Login
login = LoginManager(app)
login.login_view = 'login'

model = torch.hub.load("ultralytics/yolov5", "yolov5s", force_reload=False)  # force_reload to recache

#Bootstrap
bootstrap = Bootstrap(app)

from app import routes, models