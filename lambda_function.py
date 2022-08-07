from datetime import datetime as dt
import json
from automated_form import duplicate_form, get_next_saturday, update_form, send_message_to_line


def lambda_handler():
    today = dt.today()
    week = today.strftime("%U")

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


lambda_handler()
