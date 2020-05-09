from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate


from volunteers_help.config import BaseConfig


app = Flask(__name__)
app.config.from_object(BaseConfig)
db = SQLAlchemy(app)
migrate = Migrate(app, db)


from volunteers_help.views import *
from volunteers_help.models import District, Street, Volunteer


# District.init_district()
# Volunteer.init_volunteer()
# Street.init_street_volonteers()
