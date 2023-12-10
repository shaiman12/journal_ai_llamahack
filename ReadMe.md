
# Set up instructions
1. Make a file called api_keys.py in the root directory
2. Copy the following into the file with your api_keys listed from below in data_streams/api_keys.py
```
whatsapp_message = """ """
spotify_client_id = ""
spotify_client_secret = ""
```
3. Install all the requirements from requirements.txt
4. Do all of the following


# Setup OpenAI GPT API
1. Open Terminal: You can find it in the Applications folder or search for it using Spotlight (Command + Space).
2. Edit Bash Profile: Use the command nano ~/.bash_profile or nano ~/.zshrc (for newer MacOS versions) to open the profile file in a text editor.
3. Add Environment Variable: In the editor, add the line below, replacing your-api-key-here with your actual API key:
```
export OPENAI_API_KEY='your-api-key-here'
```
4. Save and Exit: Press Ctrl+O to write the changes, followed by Ctrl+X to close the editor.
5. Load Your Profile: Use the command source ~/.bash_profile or source ~/.zshrc to load the updated profile.
6. Verification: Verify the setup by typing echo $OPENAI_API_KEY in the terminal. It should display your API key.

# Install iMessage Importer
1. [Install Cargo](https://doc.rust-lang.org/cargo/getting-started/installation.html)
2. Run the following command:
```
cargo install imessage-exporter
```
3. Make 'imessage' directory in the data directory
4. Ensure full disk access is enabled for your terminal emulator in System Settings > Security and Privacy > Full Disk Access - enable terminal and vscode

# Whatsapp message Importer
Whatsapp installation is harder to do because it is required that you setup a whatsapp business app.

The whatsapp messages is currently limited to 100 messages from each of 100 of your latest chats 



1. Set up a directory 'data' and within that create another directory named 'whatsapp'
2. Within the 'whatsapp' directory create a text file named 'whatsapp_data.txt'
3. clear out all of your whatsapp web instances on your mobile device
4. Create a whatsapp business account for yourself
5. [Set up a Meta Developer account](https://developers.facebook.com/docs/whatsapp/cloud-api/get-started)
6. [Set up a business app](https://developers.facebook.com/docs/development/create-an-app/)
7. Add whatsapp to your business
8. On https://developers.facebook.com/apps/?show_reminder=true, select your app
9. On the left panel, select whatsapp, then select API setup, and enter your phone number as the recipient phone number
10. Copy, the command line script from the panel that says "Send messages with the API", save this for later
11. In this panel, select 'create your own message template'
12. Create a new template, select Marketing, select custom
13. Name your template 'chats'
14. Select English (US) as the language, then select next 
15. In the body of of the template write the following: '!chats'
16. Submit, and wait around an hour for approval.
17. Once approved, add the coppied command line instruction from instruction step 10 to your api_keys.py under the variable 'whatsapp_message'
18. In the api_keys.py, change the name of the template in the copied string from 'hello_world' to 'chats'
19. When you run the program make sure to have your phone ready to scan the whatsapp web QR Code

# Setup Spotify API 
1. [Create an App on Spotify Web API](https://developer.spotify.com/dashboard)
2. Make sure to select 'web api'
3. App name is: 'journal'
4. Create your own description 
5. Set redirect link to 'https://tech.cornell.edu/'
6. Your access token is only valid for one hour strecthes so you will need to replace it every time the program is run 
7. Go to your dashboard settings and copy your client id and secret_key to the api_keys.py file