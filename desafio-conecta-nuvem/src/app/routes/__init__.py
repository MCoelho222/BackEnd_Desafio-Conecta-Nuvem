from flask import Flask
from src.app.controllers.users import users
from src.app.controllers.contacts import contacts


def routes(app: Flask):
    app.register_blueprint(users)
    app.register_blueprint(contacts)