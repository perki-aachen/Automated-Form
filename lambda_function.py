#!/usr/bin/env python3
from datetime import datetime as dt
import json
#from automated_form import duplicate_form, get_next_saturday, update_form, send_message_to_line
from perkichat import PerkiChat as pc


def lambda_handler():
    today = dt.today()
    week = today.strftime("%U")

    # Initializer chatter, an instance of the PerkiChat class
    mode = 'mita'
    sender = 'AutomatedForm'
    chatter = pc(mode, sender)

    msg = "Jangan stress Pandya, semangat!"
    chatter.send_message(msg)
    # chatter.send_message(msg, img)
    """
    # Duplicate Form
    result = duplicate_form(week=week)
    print(json.dumps(result, indent=2))

    # Update Form
    satur_date = get_next_saturday(today, 5)
    str_date = satur_date.strftime("%d %B %Y")
    res = update_form(date=str_date, result=result)
    print(json.dumps(res, indent=2))
    res_uri = res["responderUri"]
    print(res_uri)

    # Send Message to Line
    send_message_to_line(res_uri)
    """


if __name__ == "__main__":
    lambda_handler()
