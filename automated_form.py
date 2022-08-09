from __future__ import print_function

import os.path

from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build

from apiclient import discovery
from httplib2 import Http
from oauth2client import client, file, tools

from datetime import timedelta

# If modifying these scopes, delete the file token.json.
SCOPES = ['https://www.googleapis.com/auth/drive']
DISCOVERY_DOC = "https://forms.googleapis.com/$discovery/rest?version=v1"


def get_next_saturday(start_date, weekday):
    time = timedelta((7 + weekday - start_date.weekday()) % 7)
    saturdate = start_date + time

    return saturdate


def duplicate_form(week):
    """Shows copy file example in Drive v3 API.
    Prints the name, id and other data of the copied file.
    """
    creds = None
    if os.path.exists('token.json'):
        creds = Credentials.from_authorized_user_file('token.json', SCOPES)
    # If there are no (valid) credentials available, let the user log in.
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file(
                'client_secrets.json', SCOPES)
            creds = flow.run_local_server(port=58415)
        # Save the credentials for the next run
        with open('token.json', 'w') as token:
            token.write(creds.to_json())

    service = build('drive', 'v3', credentials=creds)

    # Call the Drive v3 API
    origin_file_id = r'1BT3pR_3IG8RPQ1ryrKRUmyFkHt-SxHls1qKWYNGbbk4'  # example ID
    copied_file = {'name': f'Week {week} - Formulir Pendaftaran Ibadah'}
    results = service.files().copy(
        fileId=origin_file_id, body=copied_file).execute()

    return results


def update_form(date, result):
    # Request body to add description to a Form
    update = {
        "requests": [{
            "updateFormInfo": {
                "info": {
                    "title": f"Formulir Pendaftaran Ibadah {date}",
                },
                "updateMask": "title"
            }
        }]
    }

    store = file.Storage('token.json')
    creds = None
    if not creds or not creds.valid:
        flow = client.flow_from_clientsecrets('client_secrets.json', SCOPES)
        creds = tools.run_flow(flow, store)

    form_service = discovery.build('forms', 'v1', http=creds.authorize(
        Http()), discoveryServiceUrl=DISCOVERY_DOC, static_discovery=False)

    # Update the form with a description
    question_setting = form_service.forms().batchUpdate(
        formId=result["id"], body=update).execute()

    # Print the result to see it now has a description
    getresult = form_service.forms().get(formId=result["id"]).execute()

    return getresult


def send_message_to_line(uri):
    from py_topping.general_use import lazy_LINE

    # Create Class
    # Pelayanan Umum Token
    # token = 'obhJ7x4aa7tsDJ8awbUckLGNLRaLwi8TF5F3BznFZfU'
    # Perki Aachen Token
    token = 'tR5VANICCGGEcH2Vg9zj8CacFUxxdSORvp1OZPveapV'
    # Mita Token
    # token = '6iveKXRAOsMumXqa2U1kfDKBmcqlTHDKLOYJfG8e12L'
    line = lazy_LINE(token=token)

    # Send message
    line.send(f'\nShalom dan selamat pagi,\n\nbagi teman-teman yang ingin datang ke ibadah minggu ini bisa mengisi '
              f'google form di bawah ini. Selamat beraktivitas, Tuhan Yesus memberkati! ❤️\n\n{uri}',
              notification=True)

