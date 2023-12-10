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

# This function reads the CSV file and calculates the required statistics
def analyze_wearable_data(file_path):
    # Read the CSV file
    df = pd.read_csv(file_path)
    
    # Convert the 'Workout start time' column to datetime for filtering
    df['Workout start time'] = pd.to_datetime(df['Workout start time'])
    
    # Calculate overall averages
    overall_averages = {
        'Average Duration': df['Duration (min)'].mean(),
        'Average Energy Burned': df['Energy burned (cal)'].mean(),
        'Average Heart Rate': df['Average HR (bpm)'].mean(),
        'Average HR Zone 1 %': df['HR Zone 1 %'].mean(),
        'Average HR Zone 2 %': df['HR Zone 2 %'].mean(),
        'Average HR Zone 3 %': df['HR Zone 3 %'].mean(),
        'Average HR Zone 4 %': df['HR Zone 4 %'].mean(),
        'Average HR Zone 5 %': df['HR Zone 5 %'].mean(),
        'Average Activity Strain': df['Activity Strain'].mean(),
    }
    
    # Filter data for the last 10 days
    ten_days_ago = datetime.now() - timedelta(days=10)
    last_10_days_df = df[df['Workout start time'] > ten_days_ago]
    
    # Calculate averages for the last 10 days
    last_10_days_averages = {
        'Last 10 Days Average Duration': last_10_days_df['Duration (min)'].mean(),
        'Last 10 Days Average Energy Burned': last_10_days_df['Energy burned (cal)'].mean(),
        'Last 10 Days Average Heart Rate': last_10_days_df['Average HR (bpm)'].mean(),
        'Last 10 Days Average HR Zone 1 %': last_10_days_df['HR Zone 1 %'].mean(),
        'Last 10 Days Average HR Zone 2 %': last_10_days_df['HR Zone 2 %'].mean(),
        'Last 10 Days Average HR Zone 3 %': last_10_days_df['HR Zone 3 %'].mean(),
        'Last 10 Days Average HR Zone 4 %': last_10_days_df['HR Zone 4 %'].mean(),
        'Last 10 Days Average HR Zone 5 %': last_10_days_df['HR Zone 5 %'].mean(),
        'Last 10 Days Average Activity Strain': last_10_days_df['Activity Strain'].mean(),
    }
    
    # Combine overall and last 10 days averages
    combined_averages = {**overall_averages, **last_10_days_averages}
    
    return combined_averages

# Function to add the analyzed data to the user profile
def add_data_to_profile(username, analyzed_data, profiles):
    if username in profiles:
        profiles[username]['workouts_data'] = analyzed_data
    else:
        print(f"No profile found for username: {username}")
    return profiles

file_path = 'my_whoop_data_2023_12_10/workouts.csv'  # Replace with your CSV file path
username = 'jioffe502' 
profiles_file_name = 'user_profiles.json'  # The JSON file containing user profiles
profiles = load_user_profiles(profiles_file_name)

# Check if the user profile exists
if username in profiles:
    # Analyze the wearable data
    analyzed_data = analyze_wearable_data(file_path)

    # Add analyzed data to the user profile
    profiles = add_data_to_profile(username, analyzed_data, profiles)

    # Print out the updated profile with the new wearable data
    print(profiles[username])

    # Attempt to save the updated profiles back to the JSON file
    try:
        with open(profiles_file_name, 'w') as file:
            json.dump(profiles, file, indent=4)
        print(f"Profile data saved successfully to {profiles_file_name}")
    except Exception as e:
        print(f"An error occurred while saving to {profiles_file_name}: {e}")
else:
    print(f"Profile for username {username} was not found.")