import datetime
import os
import json

def read_weekly_data(past_days:int = 7):
    today = datetime.date.today()
    seven_days_ago = today - datetime.timedelta(days=7)

    # Dictionary to hold the data read from files
    data = {}

    # Loop through each day in the past 7 days
    for i in range(past_days+1):
        date = seven_days_ago + datetime.timedelta(days=i)
        file_name = date.strftime("%Y-%m-%d") + ".txt"
        relative_path = "./journals/"
        file_path = os.path.join(relative_path, file_name)

        # Check if the file exists and read it
        if os.path.exists(file_path):
            with open(file_path, 'r') as file:
                data[date.strftime("%Y-%m-%d")] = file.read()

    return json.dumps(data, indent=2)

    