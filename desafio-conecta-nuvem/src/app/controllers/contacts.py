


from flask import Blueprint
# from flask import request
# from google_auth_oauthlib.flow import Flow
from bson import json_util, ObjectId
from flask.wrappers import Response
from src.app.services.quickstart import main
from src.app import mongo_client

contacts = Blueprint("contacts", __name__, url_prefix="/contacts")

@contacts.route("/", methods=['GET'])
def list_contacts():
    # return 'Hello, world'
    try:
        user_info = main()
        print(user_info)
        user = user_info['profile']
        user_exists = mongo_client.users.find_one({'email': user['email']})
        print(user['email'])
        if not user_exists:
            mongo_client.users.insert_one(user)
            user_created = mongo_client.users.find_one({'email': user['email']})
            contacts = user_info['contacts']
            # print('HEY', contacts)
            print(user_created)
            contacts_info = {
                'user_id': user_created['_id'],
                'contacts': contacts
                }
            mongo_client.contacts.insert_one(contacts_info)
        return Response(
            response=json_util.dumps(user_info),
            status=200,
            mimetype="application/json")
    except Exception as e:
        print(e)
        return {'error': 'Something went wrong...'}, 500

