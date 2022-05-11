import datetime
import logging
from google.auth import load_credentials_from_file
from googleapiclient.discovery import build

import settings

SCOPES = ["https://www.googleapis.com/auth/calendar"]


def add_posted_event(user_name, enter_time, leave_time):
    """Add posted event at the primary calendar"""
    # Read credential file.
    creds = load_credentials_from_file(settings.GOOGLE_CLEDENTIALS_PATH, SCOPES)[0]
    # Generate Calender API Client
    service = build("calendar", "v3", credentials=creds)

    # Call the Calendar API
    now = datetime.datetime.utcnow()
    body = {
        "summary": user_name,
        "location":"",
        "start": {
            # Add `Z` at the end of the timestamp to show it is utc time.
            "dateTime": enter_time.isoformat(),
            "timeZone": "Asia/Tokyo",
        },
        "end": {
            "dateTime": leave_time.isoformat(),
            "timeZone": "Asia/Tokyo",
        },
    }
    try:
        event = (
            service.events()
                .insert(
                calendarId=settings.GOOGLE_CALENDER_ID,
                body=body,
            )
                .execute()
        )
    except Exception as e:
        logging.error(e.with_traceback())
        event = None
    return event
