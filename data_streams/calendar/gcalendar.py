from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
import os
import datetime

# Path to your client_secret.json
CLIENT_SECRET_FILE = './data_streams/calendar/client_secret.json'
SCOPES = ['https://www.googleapis.com/auth/calendar.readonly']

def authenticate_google():

    flow = InstalledAppFlow.from_client_secrets_file(CLIENT_SECRET_FILE, SCOPES)

    print("flow ",flow)

    creds = flow.run_local_server(port=8080)
    return creds

def get_calendar_events(creds):
    service = build('calendar', 'v3', credentials=creds)
    now = datetime.datetime.utcnow().isoformat() + 'Z'  # 'Z' indicates UTC time
    print('Getting the upcoming 10 events')
    events_result = service.events().list(calendarId='primary', timeMin=now,
                                          maxResults=10, singleEvents=True,
                                          orderBy='startTime').execute()
    events = events_result.get('items', [])
    events_with_start_times = []

    if not events:
        print('No upcoming events found.')
    for event in events:
        start = event['start'].get('dateTime', event['start'].get('date'))
        events_with_start_times.append(str(start) + " " + str(event['summary']) )

    print("events_with_start_times ",events_with_start_times)

    final_events_array_string = ' '.join(events_with_start_times)

    print("final_events_array_string ",final_events_array_string)
    return final_events_array_string

def get_calendar_data():
    creds = authenticate_google()
    events = get_calendar_events(creds)
    return events