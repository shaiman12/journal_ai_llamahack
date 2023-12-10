import requests
from data_streams.api_keys import weather 

def get_location():
    try:
        response = requests.get('http://ip-api.com/json/').json()
        return response['lat'], response['lon'], response['city']
    except requests.RequestException:
        return None, None, None

def get_weather(lat, lon, api_key):
    try:
        units = 'metric'
        weather_url = f"https://api.openweathermap.org/data/3.0/onecall?lat={lat}&lon={lon}&appid={api_key}&units={units}"
        weather_data = requests.get(weather_url).json()
        return weather_data
    except requests.RequestException:
        return None

def get_weather_data():

    api_key = weather

    lat, lon, city = get_location()
    if lat and lon:
        weather_data = get_weather(lat, lon, api_key)
        if weather_data:
            print("Got weather data")
            output = "The city I was in today is " + city + ". The weather in " + city + " has the description of: "
            temp = weather_data['current']['temp']
            feels_like = weather_data['current']['feels_like']
            description = weather_data['current']['weather'][0]['description']
            output += description + ". The temperature was " + str(temp) + "°C, but it felt like " + str(feels_like) + "°C."
            print(output)
            return output
        else:
            print("Error: Could not retrieve weather data.")
    else:
        print("Error: Could not determine your location.")

