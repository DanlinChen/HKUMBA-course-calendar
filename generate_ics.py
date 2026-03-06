import pandas as pd
from datetime import datetime

df = pd.read_csv("courses.csv")

def parse_dates(s):
    parts = [p.strip() for p in s.split(",")]
    first = parts[0]
    year = int(first.split()[0])
    month = first.split()[1]
    day = int(first.split()[2])

    dates = [datetime.strptime(f"{year} {month} {day}", "%Y %b %d")]
    current_month = month

    for p in parts[1:]:
        tokens = p.split()
        if len(tokens) == 2:
            current_month = tokens[0]
            day = int(tokens[1])
        else:
            day = int(tokens[0])
        dates.append(datetime.strptime(f"{year} {current_month} {day}", "%Y %b %d"))

    return dates

events = []

for _, row in df.iterrows():
    for d in parse_dates(row["日期"]):
        start = d.replace(hour=9, minute=30)
        end = d.replace(hour=18, minute=30)
        events.append((row["课程"], start, end))

def fmt(dt):
    return dt.strftime("%Y%m%dT%H%M%S")

lines = [
"BEGIN:VCALENDAR",
"VERSION:2.0",
"PRODID:-//Course Calendar//EN",
"X-WR-CALNAME:HKU MBA Courses"
]

for title, start, end in events:
    lines += [
        "BEGIN:VEVENT",
        f"SUMMARY:{title}",
        f"DTSTART:{fmt(start)}",
        f"DTEND:{fmt(end)}",
        "END:VEVENT"
    ]

lines.append("END:VCALENDAR")

open("calendar.ics","w").write("\n".join(lines))
