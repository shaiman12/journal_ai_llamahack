import json
import os
from model_apis.chatgpt import send_to_chatgpt
from data_streams.imessage import get_imessage_data
from data_streams.whatsapp import get_whatsapp_data
from data_streams.spotify import get_spotify_data
from data_streams.whoop import get_whoop_data
from data_streams.weather import get_weather_data
from data_streams.calendar.gcalendar import get_calendar_data
from data_streams.strava import get_strava_data
from datetime import datetime
import time
from analytics_response import Analytics


imesssage = True
whatsapp = False
spotify = True
grateful = True
weather = True
calendar = True
strava = False 
gpt = True
llama = True
whoop = True


def generate_therapeutic_questions():
    analytics = Analytics()
    sent_scores = analytics.get_sent_scores()

    # Analyze sentiment scores to create a summary
    max_score = max(sent_scores)
    min_score = min(sent_scores)
    avg_score = sum(sent_scores) / len(sent_scores)

    summary = "This week's sentiment journey showed "
    if avg_score > 8:
        summary += "overall positivity with few low points. "
    elif avg_score < 5:
        summary += "a challenging week with some tough days. "
    else:
        summary += "a mix of highs and lows. "

    if max_score > 8:
        summary += "The peak points suggest moments of great joy or success. "
    if min_score < 4:
        summary += "The low points indicate some struggles or challenges. "

    # Craft a prompt for GPT to generate reflective questions
    prompt = f"Based on the following sentiment summary of the week: '{summary}', generate three therapeutic and reflective questions to help introspect and plan for the upcoming week in a new section titled For the Upcoming Week. Please align the format with the current journal output into a format that is easily convertible into Notion's note application block structure, but do not mention that you are reformatting it for notion purposes. "
    
    # Send this prompt to your GPT model
    return prompt

def main():
    model_choice = eval(input("Which model would you like to use? (1 for GPT, 2 for Llama-2)\n"))
    if model_choice == 1:
        gpt = True
        llama = False
    elif model_choice == 2:
        gpt = False
        llama = True


    imessage = input("Would you like to use iMessage? (yes/no)\n").lower() == 'yes'
    whatsapp = input("Would you like to use WhatsApp? (yes/no)\n").lower() == 'yes'
    spotify = input("Would you like to use Spotify? (yes/no)\n").lower() == 'yes'
    grateful = input("Would you like to use the Grateful feature? (yes/no)\n").lower() == 'yes'
    weather = input("Would you like to access Weather information? (yes/no)\n").lower() == 'yes'
    calendar = input("Would you like to use the Calendar? (yes/no)\n").lower() == 'yes'
    strava = input("Would you like to use Strava? (yes/no)\n").lower() == 'yes'
    whoop = input("Would you like to use Whoop? (yes/no)\n").lower() == 'yes'


    prompt = """You are going to make a diary entry for me about my day today with ten different bullet points. I will provide you with a few sources of information to collate my diary entry for me. This information will come from many sources such as my iMessage conversations, my Whatsapp conversations, weather information and my Spotify. It is your job to find what would be the ten most important points to mention. It is okay for you to try infer some emotions for certain events, based on the information you have received. The diary entry should be in bullet point form, and should have exactly 10 bullet points. Make it seem as if this information is not coming from text messages, and rather a journal entry I can refer back to later. Try be as specific as possible, so that I can refer back to it ten years later and remember what I did on that day."""
    if grateful:
        prompt += "I am grateful for many things in my life. It is your job to determine 3 things I am should be grateful for, and to include this list in my diary entry. Remember that this is additional to the ten diary entries\n"
    prompt += """Here is the information you can use to create this diary entry in the first person:\n\n"""
    
    if weather:
        prompt += "Weather information:\n"
        prompt += get_weather_data()
        prompt += "\n"

    if imesssage:
        prompt += "iMessage conversations:\n"
        prompt += get_imessage_data()
        prompt += "\n"

    if whatsapp:
        prompt += "Whatsapp conversations:\n"
        prompt += get_whatsapp_data()
        prompt += "\n"

    if spotify:
        prompt += "The whatsapp conversations are over. Spotify song section begins here:\n"
        prompt += get_spotify_data()
        prompt += "\n"

    if calendar:
        print("Getting calendar data")
        prompt += "The spotify song section is over. Calendar section begins here:\n"
        prompt += get_calendar_data()
        prompt += "\n"

    if whoop:
        prompt += "The spotify song section is over. Whoop section begins here:\n"
        prompt += get_whoop_data()
        prompt += "\n"

    if strava:
        prompt += "The WHOOP section is over. Can you give me any insights on additional run data? Strava begins here"
        prompt += get_strava_data()
        prompt += "\n"
    
    prompt += "Remember to have 10 seperate diary entries. Please post-process and structure the output into a format that is easily convertible into Notion's note application block structure, but do not mention that you are reformatting it for notion purposes. Please format the diary entry as follows: 1. Start with a bold title 'Diary Entry for Today:' 2. List 10 diary entries, each starting with a number followed by a period. These should be concise and specific as mentioned previously given the data. 3. After the diary entries, add a bold title 'Gratefulness List:', and list the three things I'm grateful for today, each starting with a number followed by a period. 4. Conclude with a bold title 'Reflection:', followed by the brief paragraph summarizing the day or offering a motivational thought.\n Each section should be separated by a blank line for clarity. Structure the content to resemble journal entries with clear, distinct sections, suitable for easy reading and future reference."
    
    prompt += generate_therapeutic_questions()


    print("XXXXXXXXXXXX\n\n\n\n")
    print(prompt)
    print("XXXXXXXXXXXX\n\n\n\n")
    response = send_to_chatgpt(prompt)
    print(response)
    today_date = datetime.now().strftime("%Y-%m-%d")
    filename = f"journals/{today_date}.txt"
    with open(filename, 'w') as file:
        file.write(response)


if __name__ == "__main__":
    main()

