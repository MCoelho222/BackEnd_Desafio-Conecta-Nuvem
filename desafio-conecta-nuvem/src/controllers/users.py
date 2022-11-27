import os
import json
import requests
from datetime import datetime, timedelta
from flask import Blueprint
from flask.wrappers import Response
from flask import request, current_app
from flask.globals import session
from google_auth_oauthlib.flow import Flow
from google import auth
from google.oauth2 import id_token
from werkzeug.utils import redirect
from src.utils import generate_jwt


CLIENT_SECRETS_FILENAME = os.environ.get("GOOGLE_CLIENT_SECRETS")


users = Blueprint("users", __name__, url_prefix="/users")

flow = Flow.from_client_config(
  client_config=json.loads(CLIENT_SECRETS_FILENAME),
  scopes=[
    "https://www.googleapis.com/auth/userinfo.email",
    "https://www.googleapis.com/auth/userinfo.profile",
    "openid"
  ],
  redirect_uri = "http://localhost:5000/users/callback"
)

@users.route("/auth/google", methods=["POST"])
def auth_google():
    authorization_url, state = flow.authorization_url()
   
    session["state"] = state

    return Response(
          response=json.dumps({"url": authorization_url}),
          status=200,
          mimetype="application/json",
        )


@users.route("/callback", methods=["GET"])
def callback():
    flow.fetch_token(authorization_response=request.url)
    credentials = flow.credentials
    request_session = requests.session()
    token_google = auth.transport.requests.Request(session=request_session)
    
    # print(credentials.id_token)
    
    user_google_dict = id_token.verify_oauth2_token(
        id_token=credentials.id_token,
        request=token_google,
        audience=current_app.config["GOOGLE_CLIENT_ID"],
        clock_skew_in_seconds=2
    )

    # email = user_google_dict["email"]
    name = user_google_dict["name"]

    #user_google_dict["roles"] = ["READ", "WRITE"]
    # session["google_id"] = user_google_dict.get("sub")
    session['exp'] = datetime.utcnow() + timedelta(days=1)
    del user_google_dict["aud"]
    del user_google_dict["azp"]

    token = generate_jwt(user_google_dict)

    return redirect(f"{current_app.config['FRONTEND_URL']}#/users/{token}")

