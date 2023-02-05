from flask import Flask, make_response, request
from waitress import serve
import logging
import os

from calendar_builder import CalendarBuilder
from date_provider import DateProvider
from cache import Cache

app = Flask(__name__)
provider = DateProvider(os.environ["STREET"], os.environ["STREET_NUMBER"])
cache = Cache(60 * int(os.environ.get("CACHE_DURATION", "1")), lambda: generate_calendar(provider.fetch_dates()))


def generate_calendar(data):
    calendar_builder = CalendarBuilder()

    for waste_type, dates in data.items():
        for date in dates:
            year = date.split(".")[2]
            month = date.split(".")[1]
            day = date.split(".")[0]

            print(waste_type.value)

            calendar_builder.add_event(waste_type.value[1],
                                       [year, month, day, os.environ.get("CALENDAR_START", "7")],
                                       [year, month, day, os.environ.get("CALENDAR_END", "11")])

    calendar_builder.add_pull_recommendation(int(os.environ.get("CALENDAR_PULL_INTERVAL", "24")))

    return calendar_builder.build()


@app.route('/calendar')
def calendar():
    if "User-Agent" in request.headers and "Microsoft Outlook" in request.headers["User-Agent"]:
        logging.debug("[+] Pull from Outlook")
    else:
        logging.debug(f"[+] Pull from {request.remote_addr}")

    response = make_response(cache.get())
    response.headers["Content-Disposition"] = "attachment; filename=calendar.ics"
    response.mimetype = "text/calendar"

    return response


def main():
    # Setup logger
    log_level = os.environ.get("LOG_LEVEL", "INFO").upper()
    logging.basicConfig(level=log_level, format="%(asctime)s %(message)s")

    # Run app
    serve(app, host="0.0.0.0", port=8080)


if __name__ == '__main__':
    main()
