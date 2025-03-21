from datetime import date, datetime
from io import BytesIO
import json
import zlib

import requests
import vobject

from fastapi import FastAPI
from fastapi.responses import StreamingResponse, PlainTextResponse


app = FastAPI()

@app.get("/ical")
async def download_ical():
    headers = {
        "Content-Disposition": "attachment; filename=illustar.ics",
    }
    cal = vobject.iCalendar()
    res = requests.get("https://api.illustar.net/v1/concert?row_per_page=30&page=1&keyword=")
    data = json.loads(zlib.decompress(bytes(res.json()["data"].values())))
    for event in data["list"]:
        vevent = cal.add("vevent")
        vevent.add("summary").value = event["name"]
        vevent.add("location").value = event["place"]
        vevent.add('dtstart').value = datetime.fromisoformat(event["start_date"])
        vevent.add('dtend').value = datetime.fromisoformat(event["end_date"])
    return StreamingResponse(BytesIO(cal.serialize().encode("utf-8")),
                             headers=headers,
                             media_type="text/calendar; charset=utf-8")

@app.get("/ping")
async def ping():
    return PlainTextResponse("pong!")


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
