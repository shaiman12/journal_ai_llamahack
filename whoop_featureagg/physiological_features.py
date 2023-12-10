import pandas as pd
from datetime import datetime, timedelta
import os
import json

# Function to read user profiles from JSON file
def load_user_profiles(file_name):
    if os.path.exists(file_name):
        with open(file_name, 'r') as file:
            return json.load(file)
    else:
        print(f"The file {file_name} does not exist.")
        return {}


def analyze_recovery_data(file_path):
    # Read the CSV file
    df = pd.read_csv(file_path)
    
    # Assuming 'Cycle start time' is the column to filter last 10 days data
    df['Cycle start time'] = pd.to_datetime(df['Cycle start time'])
    
    # Calculate overall averages for the 7 key statistics
    overall_averages = {
        'Average Recovery Score %': df['Recovery score %'].mean(),
        'Average Resting Heart Rate': df['Resting heart rate (bpm)'].mean(),
        'Average Heart Rate Variability': df['Heart rate variability (ms)'].mean(),
        'Average Sleep Performance %': df['Sleep performance %'].mean(),
        'Average Asleep Duration': df['Asleep duration (min)'].mean(),
        'Average Deep Sleep Duration': df['Deep (SWS) duration (min)'].mean(),
        'Average Sleep Consistency %': df['Sleep consistency %'].mean(),
    }
    
    # Filter data for the last 10 days
    ten_days_ago = datetime.now() - timedelta(days=10)
    last_10_days_df = df[df['Cycle start time'] > ten_days_ago]
    
    # Calculate averages for the last 10 days
    last_10_days_averages = {
        'Last 10 Days Average Recovery Score %': last_10_days_df['Recovery score %'].mean(),
        'Last 10 Days Average Resting Heart Rate': last_10_days_df['Resting heart rate (bpm)'].mean(),
        'Last 10 Days Average Heart Rate Variability': last_10_days_df['Heart rate variability (ms)'].mean(),
        'Last 10 Days Average Sleep Performance %': last_10_days_df['Sleep performance %'].mean(),
        'Last 10 Days Average Asleep Duration': last_10_days_df['Asleep duration (min)'].mean(),
        'Last 10 Days Average Deep Sleep Duration': last_10_days_df['Deep (SWS) duration (min)'].mean(),
        'Last 10 Days Average Sleep Consistency %': last_10_days_df['Sleep consistency %'].mean(),
    }
    
    # Combine overall and last 10 days averages
    combined_averages = {**overall_averages, **last_10_days_averages}
    
    return combined_averages

# Function to add the analyzed data to the user profile
def add_data_to_profile(username, analyzed_data, profiles):
    if username in profiles:
        profiles[username]['wearable_data'] = analyzed_data
    else:
        print(f"No profile found for username: {username}")
    return profiles

# Replace with the path to your recovery data CSV file
file_path = 'my_whoop_data_2023_12_10/physiological_cycles.csv'
username = 'jioffe502'
profiles_file_name = 'user_profiles.json'  # The JSON file containing user profiles
profiles = load_user_profiles(profiles_file_name)

# Check if the user profile exists
if username in profiles:
    # Analyze the recovery data
    recovery_data = analyze_recovery_data(file_path)
    
    # Add recovery data to the user profile
    profiles = add_data_to_profile(username, recovery_data, profiles)
    
    # Print out the updated profile with the new recovery data
    print(profiles[username])

    # Save the updated profiles back to the JSON file
    try:
        with open(profiles_file_name, 'w') as file:
            json.dump(profiles, file, indent=4)
        print(f"Profile data saved successfully to {profiles_file_name}")
    except Exception as e:
        print(f"An error occurred while saving to {profiles_file_name}: {e}")
