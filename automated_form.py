from __future__ import print_function

import os.path

from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build

from apiclient import discovery
from httplib2 import Http
from oauth2client import client, file, tools

import datetime

# If modifying these scopes, delete the file token.json.
SCOPES = ["https://www.googleapis.com/auth/drive"]
DISCOVERY_DOC = "https://forms.googleapis.com/$discovery/rest?version=v1"


def get_next_saturday(start_date, weekday):
    time = datetime.timedelta((7 + weekday - start_date.weekday()) % 7)
    saturdate = start_date + time

    return saturdate


def create_form(week: str, date: str) -> str:
    store = file.Storage("token.json")
    creds = None
    if not creds or not creds.valid:
        flow = client.flow_from_clientsecrets("client_secrets.json", SCOPES)
        creds = tools.run_flow(flow, store)

    form_service = discovery.build(
        "forms",
        "v1",
        http=creds.authorize(Http()),
        discoveryServiceUrl=DISCOVERY_DOC,
        static_discovery=False,
    )

    NEW_FORM = {
        "info": {
            "title": f"Formulir Pendaftaran Ibadah {date}",
            "documentTitle": f"Week {week} - Formulir Pendaftaran Ibadah"
        }
    }

    # Creates the initial form
    result = form_service.forms().create(body=NEW_FORM).execute()

    # Request body to add description to a Form
    ADD_DESCRIPTION = {
        "requests": [
            {
                "updateFormInfo": {
                    "info": {
                        "title": f"Formulir Pendaftaran Ibadah {date}",
                        "description": "Shalom Saudara/i,\n\nFormulir ini dikhususkan untuk Saudara/i yang akan hadir pada ibadah di gereja. Alamat gereja adalah Roermonderstraße 110, Aachen dan ibadah dimulai jam 15.30. Demi kelancaran ibadah dan menjamin ketersediaan makanan, Saudara/i mohon hadir tepat waktu. Demi menjamin ketersediaan makanan, kami memohon Saudara/i mendaftarkan diri sebelum deadline.\n\nSampai jumpa di ibadah nanti, Tuhan Yesus memberkati! ❤️",
                    },
                    "updateMask": "description",
                }
            }
        ]
    }

    # Update the form with a description
    form_service.forms().batchUpdate(
        formId=result["formId"], body=ADD_DESCRIPTION
    ).execute()

    NAME = {
        "requests": [
            {
                "createItem": {
                    "item": {
                        "title": "Nama Lengkap ",
                        "questionItem": {
                            "question": {
                                "questionId": "60e64d32",
                                "required": True,
                                "textQuestion": {},
                            }
                        },
                    },
                    "location": {"index": 0},
                }
            }
        ]
    }

    form_service.forms().batchUpdate(
        formId=result["formId"], body=NAME
    ).execute()

    FOOD_ALLERGIES = {
        "requests": [
            {
                "createItem": {
                    "item": {
                        "title": "Pantangan bahan makanan (cth. seafood, kacang, pedas, dsb)",
                        "questionItem": {
                            "question": {
                                "questionId": "1b983dbc",
                                "textQuestion": {}
                            }
                        }
                    },
                    "location": {"index": 1},
                }
            }
        ]
    }

    form_service.forms().batchUpdate(
        formId=result["formId"], body=FOOD_ALLERGIES
    ).execute()

    # CHURCH_RULES = {
    #     "requests": [
    #         {
    #             "createItem": {
    #                 "item": {
    #                     "pageBreakItem": {},
    #                     "title": "Peraturan Gereja dan Ibadah ",
    #                     "description": "Shalom Saudara/i,\n\nberikut merupakan beberapa peraturan yang harus Saudara/i taati selama di dalam gereja dan berlangsungnya ibadah:\n\n1. Saudara/i yang datang ke gereja harus dengan kondisi tubuh yang fit dan mematuhi peraturan 2G (Geimpft und Genesen) yang dikeluarkan oleh pemerintah Jerman. Saudara/i yang hanya menunjukkan Schnelltest negatif tidak diperbolehkan datang ke gereja.\n\n2. Berlaku peraturan Maskenempfehlung di gereja dan selama jalannya ibadah.\n\n3. Saudara/i harap menjaga kebersihan diri masing-masing dan menjaga jarak yang cukup.\n\n4. Saudara/i diperbolehkan menyanyi tanpa memakai masker selama jalannya ibadah.\n\nKami berharap Saudara/i dapat mematuhi peraturan-peraturan yang berlaku. Sampai jumpa di ibadah nanti, Tuhan Yesus memberkati! "
    #                 },
    #                 "location": {"index": 2},
    #             }
    #         }
    #     ]
    # }
    #
    # form_service.forms().batchUpdate(
    #     formId=result["formId"], body=CHURCH_RULES
    # ).execute()
    #
    # RULES_CONSENT = {
    #     "requests": [
    #         {
    #             "createItem": {
    #                 "item": {
    #                     "title": "Apakah Saudara/i sudah membaca dan setuju untuk mematuhi peraturan-peraturan yang tertulis diatas? ",
    #                     "questionItem": {
    #                         "question": {
    #                             "questionId": "5e1dd378",
    #                             "required": True,
    #                             "choiceQuestion": {
    #                                 "type": "RADIO",
    #                                 "options": [
    #                                     {
    #                                         "value": "Ya"
    #                                     },
    #                                     {
    #                                         "value": "Tidak"
    #                                     }
    #                                 ]
    #                             }
    #                         }
    #                     }
    #                 },
    #                 "location": {"index": 3}
    #             }
    #         }
    #     ]
    # }
    #
    # form_service.forms().batchUpdate(
    #     formId=result["formId"], body=RULES_CONSENT
    # ).execute()

    # GET the actual form
    result = form_service.forms().get(formId=result["formId"]).execute()

    return result["responderUri"]


def send_message_to_line(uri):
    from py_topping.general_use import lazy_LINE

    # Create Class
    # Pelayanan Umum Token
    # token = 'obhJ7x4aa7tsDJ8awbUckLGNLRaLwi8TF5F3BznFZfU'
    # Perki Aachen Token
    token = "tR5VANICCGGEcH2Vg9zj8CacFUxxdSORvp1OZPveapV"
    # Mita Token
    # token = '6iveKXRAOsMumXqa2U1kfDKBmcqlTHDKLOYJfG8e12L'
    line = lazy_LINE(token=token)

    hour = datetime.datetime.now().hour
    if 0 <= hour < 11:
        greeting = "pagi"
    elif 11 <= hour <= 15:
        greeting = "siang"
    elif 15 < hour < 18:
        greeting = "sore"
    else:
        greeting = "malam"

    # Send message
    line.send(
        f"\nShalom dan selamat {greeting},\n\nbagi teman-teman yang ingin datang ke ibadah minggu ini bisa mengisi "
        f"google form di bawah ini. Selamat beraktivitas, Tuhan Yesus memberkati! ❤️\n\n{uri}",
        notification=True,
    )
