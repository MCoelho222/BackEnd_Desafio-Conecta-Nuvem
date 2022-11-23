from flask import Blueprint
from flask import request
from google_auth_oauthlib.flow import Flow
from src.app.services.quickstart import main

contacts = Blueprint("contacts", __name__, url_prefix="/contacts")

# flow = Flow.from_client_secrets_file(
#     client_secrets_file="src/app/utils/credentials.json",
#     scopes=['https://www.googleapis.com/auth/contacts.readonly'],
#     redirect_uri="http://localhost:5000/contacts/callback",
# )

@contacts.route("/", methods=['GET'])
def list_contacts():
    # return 'Hello, world'
    return main()

# @contacts.route("/callback", methods=['GET'])
# def auth_google_contacts():
#     res = request.get_json()
#     print(res)
