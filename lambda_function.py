import datetime
from datetime import datetime as dt

from automated_form import (
    get_next_saturday,
    create_form,
    send_message_to_line,
)


def lambda_handler():
    today: datetime.date = dt.today()
    week: str = today.strftime("%U")
    satur_date: datetime.date = get_next_saturday(today, 5)
    str_date: str = satur_date.strftime("%d %B %Y")

    # Create a new form
    URI = create_form(week, str_date)

    # Send Message to Line
    send_message_to_line(URI)


lambda_handler()
