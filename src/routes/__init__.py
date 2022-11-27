from flask import Flask
from src.controllers.users import users
from src.controllers.people import people


def routes(app: Flask):
    app.register_blueprint(users)
    app.register_blueprint(people)