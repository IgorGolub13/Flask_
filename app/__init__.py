from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt
from flask_login import LoginManager
from flask_migrate import Migrate

app = Flask(__name__)
app.config.from_object('config')
db = SQLAlchemy(app)
bcrypt = Bcrypt(app)
migrate = Migrate(app,db)

# manager = Manager(app)
# manager.add_command('db', MigrateCommand)

login_manager = LoginManager(app)
login_manager.login_view =  'login'
login_manager.session_protection = 'strong'
login_manager.login_message_category = 'info'

from app import views, models
