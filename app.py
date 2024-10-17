from flask import Flask, render_template, request, jsonify
import requests
import os
from dotenv import load_dotenv
from fuzzywuzzy import process  # Import fuzzy matching
from src.weather import get_weather_data

# Load environment variables from .env file
load_dotenv()

# API Keys from environment variables
WEATHER_API_KEY = os.getenv('WEATHER_API_KEY')
OPENCAGE_API_KEY = os.getenv('OPENCAGE_API_KEY')

# Initialize Flask app
app = Flask(__name__)

# List of cities for fuzzy matching
city_list = ['New Delhi', 'Delhi', 'Mumbai', 'Bangalore', 'Chennai', 'Kolkata', 'Hyderabad', 'Pune', 'Jaipur',
             'Lucknow']


# Function to get suggestions with fuzzy matching
def get_fuzzy_suggestions(query):
    suggestions = process.extract(query, city_list, limit=5)  # Get top 5 matches
    return [match[0] for match in suggestions]


# Route to render the homepage
@app.route('/')
def index():
    return render_template('index.html')


# Route to handle city suggestions (with fuzzy matching)
@app.route('/suggest_cities')
def suggest_cities():
    query = request.args.get('q')
    if query:
        suggestions = get_fuzzy_suggestions(query)  # Use fuzzy matching for suggestions
        return jsonify(suggestions)
    else:
        return jsonify([])


# Route to handle weather fetching
@app.route('/get_weather', methods=['POST'])
def get_weather():
    location = request.form['location']
    weather_data = get_weather_data(location)

    if weather_data:
        temperature = weather_data['main']['temp']
        description = weather_data['weather'][0]['description']
        return f"The weather in {location}: {temperature}°C, {description}"
    else:
        return "Sorry, we couldn't fetch the weather for that location."


# Run the Flask app
if __name__ == '__main__':
    print("Starting Flask app...")
    app.run(debug=True)
