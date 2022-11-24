from flask import Flask
from src.app.controllers.users import users
from src.app.controllers.people import people


def routes(app: Flask):
    app.register_blueprint(users)
    app.register_blueprint(people)