import os
import json
import requests
from flask import Flask, render_template, jsonify, request
from datetime import datetime
from config import DATA_DIRECTORY, OPENWEATHER_API_KEY
from weather_collector import fetch_weather_data, save_weather_data

app = Flask(__name__)

@app.context_processor
def inject_now():
    """
    Inject the current datetime into all templates
    """
    return {'now': datetime.now()}

@app.route('/')
def index():
    """
    Main page - displays current weather data
    """
    return render_template('index.html')

@app.route('/api/current')
def current_weather():
    """
    API endpoint to get current weather data
    """
    data = fetch_weather_data()
    if data:
        return jsonify(data)
    return jsonify({"error": "Failed to fetch weather data"}), 500

@app.route('/api/search')
def search_city():
    """
    API endpoint to search for a city by name
    """
    city_name = request.args.get('q', '')
    if not city_name or len(city_name) < 3:
        return jsonify({"error": "Please provide a city name with at least 3 characters"}), 400
    
    if not OPENWEATHER_API_KEY:
        return jsonify({"error": "API key not configured"}), 500
    
    try:
        url = f"https://api.openweathermap.org/data/2.5/weather?q={city_name}&appid={OPENWEATHER_API_KEY}&units=metric"
        response = requests.get(url)
        response.raise_for_status()
        data = response.json()
        data['timestamp'] = datetime.now().isoformat()
        return jsonify(data)
    except requests.exceptions.RequestException as e:
        return jsonify({"error": f"Error searching for city: {str(e)}"}), 500

@app.route('/api/history')
def weather_history():
    """
    API endpoint to get historical weather data
    """
    history = []
    
    # Check if data directory exists
    if not os.path.exists(DATA_DIRECTORY):
        return jsonify(history)
    
    # Get all JSON files in the data directory
    files = [f for f in os.listdir(DATA_DIRECTORY) if f.endswith('.json')]
    files.sort(reverse=True)  # Sort by newest first
    
    # Load data from each file
    for file in files[:10]:  # Limit to 10 most recent files
        file_path = os.path.join(DATA_DIRECTORY, file)
        try:
            with open(file_path, 'r') as f:
                data = json.load(f)
                history.append({
                    'timestamp': file.replace('weather_data_', '').replace('.json', ''),
                    'data': data
                })
        except Exception as e:
            print(f"Error loading file {file}: {str(e)}")
    
    return jsonify(history)

@app.route('/history')
def history_page():
    """
    Page to display historical weather data
    """
    return render_template('history.html')

@app.route('/search')
def search_page():
    """
    Page to search for cities
    """
    return render_template('search.html')

@app.route('/save-search', methods=['POST'])
def save_search():
    """
    API endpoint to save a searched city's weather data
    """
    try:
        data = request.get_json()
        if not data:
            return jsonify({"error": "No data provided"}), 400
        
        save_weather_data([data])
        return jsonify({"success": True, "message": "Weather data saved successfully"})
    except Exception as e:
        return jsonify({"error": f"Error saving data: {str(e)}"}), 500

if __name__ == '__main__':
    # Make sure the data directory exists
    os.makedirs(DATA_DIRECTORY, exist_ok=True)
    
    # In Docker, we need to listen on 0.0.0.0
    app.run(debug=True, host='0.0.0.0') 