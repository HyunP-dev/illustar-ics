import os
from datetime import datetime
import json
import zlib

import vobject
import requests


def main():
    print("Generating ics file as output/illustar.ics")
    if not os.path.exists("output"):
        os.mkdir("output")
    cal = vobject.iCalendar()
    
    concert_res = requests.get("https://api.illustar.net/v1/concert?row_per_page=30&page=1&keyword=")
    concert_data = json.loads(zlib.decompress(bytes(concert_res.json()["data"].values())))["list"]

    event_res = requests.get("https://api.illustar.net/v1/event/list")
    event_data = json.loads(zlib.decompress(bytes(event_res.json()["data"].values())))["eventInfo"]

    for event in concert_data + event_data:
        if event["start_date"].startswith("0"):
            continue
        
        vevent = cal.add("vevent")
        vevent.add("summary").value = event["name"]
        vevent.add("location").value = event["place"]
        
        vevent.add('dtstart').value = datetime.fromisoformat(event["start_date"])
        vevent.add('dtend').value = datetime.fromisoformat(event["end_date"])

    with open("output/illustar.ics", "wb") as f:
        f.write(cal.serialize().encode("utf-8"))

    cal.prettyPrint()

main()
