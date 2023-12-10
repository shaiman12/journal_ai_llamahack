import subprocess
import time
import os
from data_streams.api_keys import whatsapp_message

def start_server():
    # Start the server and keep it running in the background
    server_command = "node data_streams/whatsapp.js"
    server_process = subprocess.Popen(server_command, shell=True)
    return server_process


def run_second_command():
    # Run your second command here
    second_command = whatsapp_message
    subprocess.Popen(second_command, shell=True)


def stop_server(server_process):
    # Terminate the server process
    server_process.kill()



def open_image(image_path):
    # Open the image with the default image viewer
    if os.name == 'nt':  # for Windows
        os.system(f'start {image_path}')
    else:  # for macOS and Linux
        os.system(f'open {image_path}' if os.name == 'posix' else f'xdg-open {image_path}')

def get_whatsapp_data():
    file_path = 'data/whatsapp/whatsapp_data.txt'
    image_path = 'qr.png'


    # Open the file in write mode, which clears the contents
    with open(file_path, 'w'):
        pass


    # Start the server
    server_process = start_server()

    time.sleep(30)

    # Open the QR code image
    open_image(image_path)

    time.sleep(60)

    # Run the second command
    run_second_command()

    # Additional code or a condition to determine when to stop the server
    # ...
    print("Getting Whatsapp Chats...")
    time.sleep(120)
    # Stop the server
    stop_server(server_process)

    message = "These are the Whatsapp messages from today. All the messages sent by me will start with 'me' and all the messages sent by the other person will start with 'other person'. Please be selective with which group conversations to use in your generation of my diary entry. You should mostly only use group conversations in which I send messages.\n\n"

    # Use with statement to ensure the file is properly closed after reading
    with open(file_path, 'r', encoding='utf-8') as file:
        file_contents = file.read()
    message += file_contents
    return message