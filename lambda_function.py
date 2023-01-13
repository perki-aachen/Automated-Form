import datetime
from datetime import datetime as dt
from datetime import timedelta

from automated_form import (
    get_next_saturday,
    create_form,
    send_message_to_line,
)


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


if __name__ == "__main__":
    create_multiple_forms()
