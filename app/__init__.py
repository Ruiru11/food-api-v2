from flask import Flask
from flask_bcrypt import Bcrypt
from .config import configuration

bcrypt = Bcrypt()

from app.models.Database import Database_connection
from app.views.orders import mod_orders
from app.views.users import mod_users
from app.views.menus import mod_menus

db = Database_connection()


def create_app(environment):
    app = Flask(__name__)
    app.config.from_object(configuration[environment])
    app.register_blueprint(mod_orders)
    app.register_blueprint(mod_users)
    app.register_blueprint(mod_menus)
    db
    return app
