from __future__ import print_function

from apiclient import discovery
from httplib2 import Http
from oauth2client import client, file, tools

from typing import Dict, List
import re

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
    form_id = '1kwBxazzw38gog8XP9WnII7E1xD9st3vZTxFemT2qp-Q'
    result = service.forms().responses().list(formId=form_id).execute()
    total_responses = result["responses"].__len__()

    allergies = get_allergic(result)
    send_responses_to_line(total_responses, allergies)


def get_allergic(response: Dict) -> List:
    allergies = []
    for res in response["responses"]:
        if res["answers"].get("1b983dbc"):
            answer = res["answers"]["1b983dbc"]["textAnswers"]["answers"][0]['value']
            if answer not in allergies and re.match("^[a-zA-Z]", answer):
                allergies.append(answer)

    return allergies


def send_responses_to_line(responses: Dict, allergies: List) -> None:
    from py_topping.general_use import lazy_LINE

    # Create Class
    # Mita Token
    token = 'obhJ7x4aa7tsDJ8awbUckLGNLRaLwi8TF5F3BznFZfU'
    # Perki Aachen Token
    # token = 'tR5VANICCGGEcH2Vg9zj8CacFUxxdSORvp1OZPveapV'
    # Pelayanan Umum Token
    # token = '6iveKXRAOsMumXqa2U1kfDKBmcqlTHDKLOYJfG8e12L'
    # Group Masak
    # token = 'CBCOw0nqUJcYYnkYbnYeoxJIRRWQ1ExOtCixtjrlq7m'
    line = lazy_LINE(token=token)
    allergies_text = '\n- '.join(map(str, allergies))
    # Send message
    line.send(f'\n\nTotal responses: {responses} People 🍱 🥳 🎉\n\nList of allergies:\n- {allergies_text}',
              notification=True)


if __name__ == '__main__':
    main()




