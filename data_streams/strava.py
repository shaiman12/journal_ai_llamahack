import requests

from datetime import datetime,timezone


# def get_strava_data():

#     # Replace with your actual Client ID, Client Secret, and Refresh Token
#     CLIENT_ID = '117942'
#     strava_client_secret = 'ec51f062212f33bd88945b8fe38adcb22b61a8f9'
#     REFRESH_TOKEN = '1a0514837153cc23bfc06c63377c65fe05095fcf'
#     REDIRECT_URI = 'http://localhost:8000'
#     access_token = "7742ba68b2028efcca1fed1b1415a54afee281f3"

    

  
#     # Using the access token to access endpoint for activities
#     activities_url = "https://www.strava.com/api/v3/athlete/activities"
#     header = {'Authorization': 'Bearer ' + access_token}
#     param = {'per_page': 200, 'page': 1}

#     activities = requests.get(activities_url, headers=header, params=param).json()

#     # Get today's date
#     today = datetime.now().date()

#     print(activities)

#     # Filter activities for today
#     today_activities = [activity for activity in activities if datetime.strptime(activity['start_date_local'][:10], '%Y-%m-%d').date() == today]
#     stringified_data = json.dumps(today_activities, indent=4)

#     return stringified_data
#     # return ""




from flask import Flask, request
import requests
import threading
import webbrowser
import json

from data_streams.api_keys import strava_client_id, strava_client_secret

# Strava API credentials
redirect_uri = 'http://localhost:8000/callback'
scope = 'read,activity:read'  # Example scope, check Strava's documentation for actual scopes

# Flask app setup
app = Flask(__name__)

# Global variable to store activities
activities_list = None

# Function to generate the authorization URL
def get_strava_auth_url():
    url = f"http://www.strava.com/oauth/authorize?client_id={strava_client_id}&response_type=code&redirect_uri={redirect_uri}&approval_prompt=force&scope={scope}"
    return url

# Function to exchange code for token
def strava_token_exchange(code):
    url = 'https://www.strava.com/oauth/token'
    payload = {
        'client_id': strava_client_id,
        'client_secret': strava_client_secret,
        'code': code,
        'grant_type': 'authorization_code'
    }
    response = requests.post(url, data=payload)
    return response.json()

# Route to handle OAuth redirect and get access token
@app.route('/callback')
def callback():
    global activities_list
    code = request.args.get('code')
    token_response = strava_token_exchange(code)
    activities_list = get_recent_activities(token_response['access_token'])
    return "Received activities list, you can close this window."

# Function to retrieve Strava activities
def get_recent_activities(access_token):
    url = 'https://www.strava.com/api/v3/athlete/activities'
    headers = {'Authorization': f"Bearer {access_token}"}
    response = requests.get(url, headers=headers)
    activities = response.json()
    today_activities = []

    # Get today's date
    today = datetime.now(timezone.utc).date()

    for activity in activities:
        # Parse the start date of the activity
        activity_date = datetime.strptime(activity['start_date'], '%Y-%m-%dT%H:%M:%SZ').date()

        # Check if the activity is from today
        if activity_date == today:
            fields_to_extract = ['name', 'distance', 'moving_time']
            activity_core_data_extracted = {field: activity[field] for field in fields_to_extract}
            today_activities.append(activity_core_data_extracted)

    #extract certain fields like name, distance, moving time



    return json.dumps(today_activities, indent=4)
    

# Function to run the Flask app
def run_app():
    app.run(port=8000)

# Function to start the Strava server and handle authentication
def run_strava_server():
    global activities_list
    # Run Flask app in a separate thread
    threading.Thread(target=run_app, daemon=True).start()

    # Open the browser for user authentication
    auth_url = get_strava_auth_url()
    webbrowser.open(auth_url)

    # Wait for the activities list to be populated
    while activities_list is None:
        pass

    return activities_list

def get_strava_data():
    activities = run_strava_server()
    print(activities)
    return activities


