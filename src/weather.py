import requests
import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

WEATHER_API_KEY = os.getenv('WEATHER_API_KEY')


def get_weather_data(location):
    # OpenWeatherMap API request URL
    url = f"http://api.openweathermap.org/data/2.5/weather?q={location}&appid={WEATHER_API_KEY}&units=metric"
    print(f"Requesting weather for {location} with URL: {url}")  # Debugging
    response = requests.get(url)

    if response.status_code == 200:
        return response.json()  # Return the JSON weather data
    else:
        print(f"Error: {response.status_code}, {response.text}")  # Log errors
        return None
