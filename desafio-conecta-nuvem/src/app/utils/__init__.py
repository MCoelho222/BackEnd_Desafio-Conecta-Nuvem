import os
import certifi
from jwt import encode
from flask import current_app
from pymongo import MongoClient

mongo = client = MongoClient(os.getenv("MONGO_URI"), tls=True, tlsCAFile=certifi.where())

def generate_jwt(payload):
    token = encode(payload, current_app.config["SECRET_KEY"], "HS256")

    return token