import uuid


class CalendarBuilder:

    def __init__(self):
        self.content = """BEGIN:VCALENDAR
VERSION:2.0
PRODID:https://github.com/Paul2708
BEGIN:VTIMEZONE
TZID:Europe/Berlin
X-LIC-LOCATION:Europe/Berlin
BEGIN:DAYLIGHT
TZOFFSETFROM:+0100
TZOFFSETTO:+0200
TZNAME:CEST
DTSTART:19700329T020000
RRULE:FREQ=YEARLY;BYDAY=-1SU;BYMONTH=3
END:DAYLIGHT
BEGIN:STANDARD
TZOFFSETFROM:+0200
TZOFFSETTO:+0100
TZNAME:CET
DTSTART:19701025T030000
RRULE:FREQ=YEARLY;BYDAY=-1SU;BYMONTH=10
END:STANDARD
END:VTIMEZONE
"""

    def add_event(self, summary, start, end):
        self.content += \
            f"""BEGIN:VEVENT
SUMMARY:{summary}
DTSTART;TZID=Europe/Berlin;VALUE=DATE-TIME:{start[0]}{start[1].zfill(2)}{start[2].zfill(2)}T{start[3].zfill(2)}0000
DTEND;TZID=Europe/Berlin;VALUE=DATE-TIME:{end[0]}{end[1].zfill(2)}{end[2].zfill(2)}T{end[3].zfill(2)}0000
DTSTAMP:{start[0]}{start[1].zfill(2)}{start[2].zfill(2)}T{start[3].zfill(2)}0000
UID:{uuid.uuid4()}
END:VEVENT
"""

    def add_pull_recommendation(self, hours):
        self.content += f"X-PUBLISHED-TTL:PT{hours}H\n"

    def build(self):
        self.content += "END:VCALENDAR"

        return self.content
