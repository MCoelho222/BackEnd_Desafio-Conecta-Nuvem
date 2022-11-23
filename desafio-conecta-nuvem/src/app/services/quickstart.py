from __future__ import print_function

import os
# import os.path
import json
from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError

CLIENT_SECRETS_FILENAME = '{"installed":{"client_id":"58306360300-s2692rj0jf884lk65l70bhj7e8ad0mcu.apps.googleusercontent.com","project_id":"compact-retina-369401","auth_uri":"https://accounts.google.com/o/oauth2/auth","token_uri":"https://oauth2.googleapis.com/token","auth_provider_x509_cert_url":"https://www.googleapis.com/oauth2/v1/certs","client_secret":"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","redirect_uris":["http://localhost"]}}'
# If modifying these scopes, delete the file token.json.
SCOPES = [
    "openid",
    'https://www.googleapis.com/auth/contacts.readonly',
    "https://www.googleapis.com/auth/userinfo.profile",
    "https://www.googleapis.com/auth/userinfo.email"
]


def main():
    """Shows basic usage of the People API.
    Prints the name of the first 10 connections.
    """
    creds = None
    # The file token.json stores the user's access and refresh tokens, and is
    # created automatically when the authorization flow completes for the first
    # time.
    if os.path.exists('token.json'):
        creds = Credentials.from_authorized_user_file('token.json', SCOPES)
    # If there are no (valid) credentials available, let the user log in.
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_config(
                client_config=json.loads(CLIENT_SECRETS_FILENAME), scopes=SCOPES)
            creds = flow.run_local_server(port=0)
        # Save the credentials for the next run
        with open('token.json', 'w') as token:
            token.write(creds.to_json())
    try:
        service = build('people', 'v1', credentials=creds)
        # Call the People API
        # print('List 10 connection names')
        
        contacts_service = service.people().connections().list(
            resourceName='people/me',
            pageSize=2000,
            personFields='emailAddresses').execute()
        connections = contacts_service.get('connections', [])
        
        user_service = service.people().get(resourceName='people/me', personFields='names,emailAddresses').execute()
        username = user_service.get('names')[0].get('displayName')
        useremail = user_service.get('emailAddresses')[0].get('value')

        user_infos = {
            'profile': {
                'name': username,
                'email': useremail
                }}

        domains = set([])
        emails = set([])
        for person in connections:
            # names = person.get('names', [])
            person_emails = person.get('emailAddresses', [])
            # print(person_emails)
            if person_emails:
                for email in person_emails:
                    value = email.get('value')
                    domain = value.split('@')[-1]
                    domains.add(domain)
                    emails.add(value)
        domains_dict = {}
        for domain in domains:
            same_domains = []
            for email in emails:
                email_domain = email.split('@')[-1]
                if email_domain == domain:
                    same_domains.append(email)
            domains_dict[domain] = same_domains
        # print(domains_dict)
        user_infos['contacts'] = domains_dict
        return user_infos
    except HttpError as err:
        print(err)


if __name__ == '__main__':
    main()