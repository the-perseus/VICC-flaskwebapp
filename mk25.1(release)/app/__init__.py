#übernommen aus microblog template.
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_login import LoginManager
from config import Config
#importiert die benötigten module für das flask app. SQLAlchemy, Migrate wird für die Verbindung zur DB benötigt.
#LoginManager wird für User AUTH benötigt
#Config importiert die config.py im root, wo die datenbank URI definiert istitle
app = Flask(__name__) #erstellt eine neue flask instanz
app.config.from_object(Config) #benutzt die config.py für die Erstellung
db = SQLAlchemy(app) #erstellt die neue DB Instanz
migrate = Migrate(app, db) #Migrationsobjekt um app und db zu übergeben
login = LoginManager(app) #für AUTH
login.login_view = 'login' #für login handling

from app import routes, models, api
#import von routes.py, models.py, api.py