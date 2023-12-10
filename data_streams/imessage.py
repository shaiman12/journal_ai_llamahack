from datetime import datetime, timedelta
import subprocess
import os
import shutil
import re

# date_today = datetime.today().strftime('%Y-%m-%d')
date_today = (datetime.now() - timedelta(days=1)).strftime('%Y-%m-%d')


def clear_directory(path):
    # Check if the directory exists
    if not os.path.isdir(path):
        print("Directory does not exist.")
        return

    for filename in os.listdir(path):
        file_path = os.path.join(path, filename)

        try:
            # If it's a file, remove it
            if os.path.isfile(file_path) or os.path.islink(file_path):
                os.unlink(file_path)
            # If it's a directory, remove it and all its contents
            elif os.path.isdir(file_path):
                shutil.rmtree(file_path)
        except Exception as e:
            print(f'Failed to delete {file_path}. Reason: {e}')


def process_message(text):
    # Remove phone numbers
    text = re.sub(r'\+\d{11}', '', text)
    # Remove attachment information
    text = re.sub(r'/Users/[\S]+', '', text)
    return text.strip()


def extract_time(line):
    # Extract only the time part from the timestamp
    match = re.search(r'\d{1,2}:\d{2}:\d{2} [AP]M', line)
    return match.group(0) if match else ''


def process_file(file_path):
    with open(file_path, 'r') as file:
        lines = file.readlines()
    
    messages = []
    current_sender = ''
    current_message = []
    current_time = ''
    for line in lines:
        line = line.strip()
        # Check if line is a date line
        if re.match(r'\w{3} \d{2}, \d{4}.*', line):
            if current_message:
                messages.append(f"{current_sender} '{current_time}': '{''.join(current_message)}'")
            current_message = []
            current_time = extract_time(line)  # Extract only the time
        elif line.startswith('Me') or re.match(r'\+\d{11}', line):
            if current_message:
                messages.append(f"{current_sender} '{current_time}': '{''.join(current_message)}'")
            current_sender = 'me' if line.startswith('Me') else 'other person'
            current_message = []
        else:
            current_message.append(process_message(line))
    
    # Add the last message
    if current_message:
        messages.append(f"{current_sender} '{current_time}': '{''.join(current_message)}'")
    
    return '\n'.join(messages)


def message_cleaner():
    directory = 'data/imessage'
    all_conversations = []
    for i, filename in enumerate(os.listdir(directory), start=1):
        file_path = os.path.join(directory, filename)
        conversation = process_file(file_path)
        all_conversations.append(f"Conversation {i}:\n{conversation}")

    final_output = '\n\n'.join(all_conversations)
    return final_output


def get_imessage_data():
    print("Getting iMessage data...")
    directory_path = "data/imessage"
    clear_directory(directory_path)
    try:
        subprocess.run(["imessage-exporter", "-f", "txt", "-o", "data/imessage", "-s", date_today], check=True)
        print("Command executed successfully.")
    except subprocess.CalledProcessError as e:
        print(f"An error occurred: {e}")
    print("iMessage data retrieved.")
    print("Cleaning iMessage data...")
    message = "These are the imessage messages from today. All the messages sent by me will start with 'me' and all the messages sent by the other person will start with 'other person'.\n\n"
    message += message_cleaner()
    return message
