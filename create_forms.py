import datetime
from datetime import datetime as dt
from datetime import timedelta

from automated_form import (
    get_next_saturday,
    create_form
)

from Google import Create_Service
import json
import pandas as pd


def create_multiple_forms():
    today: datetime.date = dt(2023, 1, 2)

    for week in range(0, 51):
        if today.isocalendar()[1] % 2 == 0:
            str_week: str = today.strftime("%U")
            saturday: datetime.date = get_next_saturday(today, 5)
            str_sat: str = saturday.strftime("%d %B %Y")
            # Create a new form
            URI = create_form(str_week, str_sat)
            print(URI)

        today: datetime.date = today + timedelta(weeks=1)


def get_forms_id():
    CLIENT_SECRET_FILE = 'client_secrets.json'
    API_NAME = 'drive'
    API_VERSION = 'v3'
    SCOPES = ['https://www.googleapis.com/auth/drive']

    service = Create_Service(CLIENT_SECRET_FILE, API_NAME, API_VERSION, SCOPES)

    FOLDER_ID = '1yrzBuqnDmmnyG_7Z6CYRjHuPB6PuvraF'

    query = f"parents = '{FOLDER_ID}'"
    response = service.files().list(q=query).execute()
    files = response.get('files')
    nextPageToken = response.get("nextPageToken")

    while nextPageToken:
        response = service.files().list(q=query, nextPageToken=nextPageToken).execute()
        files.extend(response.get('files'))
        nextPageToken = response.get('nextPageToken')

    df = pd.DataFrame(files)
    ids = df["id"].to_json('form_ids.json')

    with open('form_ids.json', 'r') as f:
        parsed = json.load(f)
        print(json.dumps(parsed, indent=4))


if __name__ == "__main__":
    # create_multiple_forms()
    get_forms_id()
