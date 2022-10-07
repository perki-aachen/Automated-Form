from __future__ import print_function

from apiclient import discovery
from httplib2 import Http
from oauth2client import client, file, tools

SCOPES = "https://www.googleapis.com/auth/forms.responses.readonly"
DISCOVERY_DOC = "https://forms.googleapis.com/$discovery/rest?version=v1"


def main():
    store = file.Storage('token.json')
    creds = None
    if not creds or creds.invalid:
        flow = client.flow_from_clientsecrets('client_secrets.json', SCOPES)
        creds = tools.run_flow(flow, store)
    service = discovery.build('forms', 'v1', http=creds.authorize(
        Http()), discoveryServiceUrl=DISCOVERY_DOC, static_discovery=False)

    # Prints the responses of your specified form:
    form_id = '16knQAqFlWQEm7M4f2OHLkqATgZL5r7SJekaTpAsrA3Q'
    result = service.forms().responses().list(formId=form_id).execute()
    total_responses = result["responses"].__len__()

    send_responses_to_line(total_responses)


def send_responses_to_line(responses):
    from py_topping.general_use import lazy_LINE

    # Create Class
    # Mita Token
    token = 'obhJ7x4aa7tsDJ8awbUckLGNLRaLwi8TF5F3BznFZfU'
    # Perki Aachen Token
    # token = 'tR5VANICCGGEcH2Vg9zj8CacFUxxdSORvp1OZPveapV'
    # Pelayanan Umum Token
    # token = '6iveKXRAOsMumXqa2U1kfDKBmcqlTHDKLOYJfG8e12L'
    line = lazy_LINE(token=token)

    # Send message
    line.send(f'\nTotal responses: {responses} People 🍱🥳🎉',
              notification=True)


if __name__ == '__main__':
    main()




