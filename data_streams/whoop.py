import time
from flask import Flask, request, redirect, session
import requests
import logging
from data_streams.api_keys import whoop_client_id, whoop_secret_id
import os
import webbrowser
import secrets
import pandas as pd
from threading import Thread
import json

# Setup basic logging
logging.basicConfig(level=logging.DEBUG)

# WHOOP API credentials
client_id = whoop_client_id
client_secret = whoop_secret_id
redirect_uri = 'http://localhost:8008/callback'
scope = 'read:recovery'
os.environ['OAUTHLIB_INSECURE_TRANSPORT'] = '1'

app = Flask(__name__)
app.secret_key = 'thishastobeovereightcharsright'

recovery_data = None

authorization_base_url = 'https://api.prod.whoop.com/oauth/oauth2/auth'
token_url = 'https://api.prod.whoop.com/oauth/oauth2/token'

@app.route('/authorize')
def authorize():
    state = secrets.token_urlsafe(16)
    session['oauth_state'] = state
    auth_url = f"{authorization_base_url}?response_type=code&client_id={client_id}&redirect_uri={redirect_uri}&scope={scope}&state={state}"
    logging.info(f"Generated state: {state}")
    return redirect(auth_url)

@app.route('/callback')
def callback():
    state = request.args.get('state')
    logging.info(f"Received state: {state}")
    logging.info(f"Session state: {session.get('oauth_state')}")

    if state != session.get('oauth_state'):
        return 'State parameter mismatch', 400

    code = request.args.get('code')
    token_response = requests.post(token_url, data={
        'grant_type': 'authorization_code',
        'code': code,
        'redirect_uri': redirect_uri,
        'client_id': client_id,
        'client_secret': client_secret
    })

    if token_response.ok:
        token_info = token_response.json()
        recovery_data = get_recovery_data(token_info['access_token'])
        logging.info(f"Recovery Data: {recovery_data}")
        with open('recovery_data.json', 'w') as file:
            json.dump(recovery_data, file)
        return "Received recovery, sleep, and workout data, you can close this window."
    else:
        logging.error(f"Error in token exchange: {token_response.text}")
        return f"Failed to exchange token: {token_response.text}", 400

def get_recovery_data(access_token):
    headers = {'Authorization': f'Bearer {access_token}'}
    response = requests.get('https://api.prod.whoop.com/developer/v1/recovery', headers=headers)
    if response.ok:
        data = response.json()
        if data and 'records' in data and data['records']:
            # Extracting the most recent record
            most_recent_record = data['records'][0]  # Assuming the first record is the most recent
            score = most_recent_record.get('score', {})
            return {
                'hrv_rmssd_milli': score.get('hrv_rmssd_milli'),
                'recovery_score': score.get('recovery_score'),
                'resting_heart_rate': score.get('resting_heart_rate')
            }
    else:
        logging.error(f"Failed to fetch recovery data: {response.text}")
        return None
    
def read_user_profile_data(user_id):
    with open('user_profiles.json', 'r') as file:
        data = json.load(file)
        return data.get(user_id, {})


def run_app():
    app.run(port=8008, threaded = True)

def start_flask_app():
    thread = Thread(target=run_app)
    thread.daemon = True
    thread.start()    

def run_whoop_server():
    global recovery_data
    auth_url = f"{authorization_base_url}?response_type=code&client_id={client_id}&redirect_uri={redirect_uri}&scope={scope}"
    logging.info(f"Auth URL: {auth_url}")
    webbrowser.open(auth_url)
    start_flask_app()  # Start Flask app normally instead of in a separate thread

def get_whoop_data():
    output = "This is my WHOOP's most important data points. Given my poor recovery today, mention how I nearly pulled an all nighter in the hackathon but its important to catch up on sleep to finish school strong! Then please identify two to three of the key highlights or trends and be a life coach! Write a brief and quippy encouraging note if I am doing well compared to my averages and if I am below average give some inspiration for me to reflect on so I can get back on track. Please have a section of my diary entry dedicated to exercise separate to all the other diary entries, and gratefulness list\n\n"
    
    # Start WHOOP server and wait for data
    run_whoop_server()
    while not os.path.exists('recovery_data.json'):
        time.sleep(1)  # Wait for 1 second before checking again

    # Read WHOOP data from the file
    with open('recovery_data.json', 'r') as file:
        data = json.load(file)

    # Append current data to the output
    if data:
        output += f"Today's HRV (RMSSD): {data['hrv_rmssd_milli']} ms\n"
        output += f"Today's Recovery Score: {data['recovery_score']}\n"
        output += f"Today's Resting Heart Rate: {data['resting_heart_rate']} bpm\n"
    else:
        output += "No current recovery data available.\n"

    # Read and append historical data
    user_profile_data = read_user_profile_data('jioffe502')
    if user_profile_data:
        wearable_data = user_profile_data.get('wearable_data', {})
        for key, value in wearable_data.items():
            output += f"{key}: {value}\n"

    return output