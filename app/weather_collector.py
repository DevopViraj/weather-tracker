import os
import json
import requests
from datetime import datetime
import time
import logging

from config import OPENWEATHER_API_KEY, CITY_IDS, DATA_DIRECTORY    

# Logging Setup
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[logging.FileHandler('weather_collector.log'),     # save logs to a file
    logging.StreamHandler()    # print logs to console
    ]
  )

# Creates own logger instead of using root logger
logger = logging.getLogger("weather_collector")


def fetch_weather_data():
    """
    Fetch current weather data for cities in CITY_IDS
    """
    if not OPENWEATHER_API_KEY:
        logger.error("No API key found. Please set OPENWEATHER_API_KEY in .env file")
        return None
    
    if not CITY_IDS:
        logger.error("CITY_IDS not found. Please set CITY_IDS in .env file")
        return None
    
    city_list = CITY_IDS.split(',')
    results = []

    for city_id in city_list:
        logger.info(f"Fetching weather data for city ID: {city_id}")
        try:
            url = f"https://api.openweathermap.org/data/2.5/weather?id={city_id}&appid={OPENWEATHER_API_KEY}&units=metric"
            response = requests.get(url)
            response.raise_for_status() # Raise an exception for HTTP errors
            data = response.json()
            data['timestamp'] = datetime.now().isoformat()
            results.append(data)
            logger.info(f"Successfully retrieved data for {data.get('name', 'unknown')} (City ID: {city_id})")

            # Letting the API rest
            time.sleep(1)
        except requests.exceptions.RequestException as e:
            logger.error(f"Error fetching data for city {city_id}: {str(e)}")
    return results
        
def save_weather_data(data):
    """
    Save weather data to JSON files
    """
    if not data:
        logger.warning("No data to save")
        return
    
    # Ensure that data directory exists
    os.makedirs(DATA_DIRECTORY, exist_ok=True)

    timestamp = datetime.now().strftime("%Y%m%d%H%M%S")
    filename = os.path.join(DATA_DIRECTORY, f"weather_data_{timestamp}.json")

    try:
        with open(filename, 'w') as file:
            json.dump(data, file, indent=2)
            logger.info(f"Data saved to {filename}\n")
    except Exception as e:
        logger.error(f"Error saving data: {str(e)}")

def main():
    """
    Main function to run the weather collector
    """
    print("Starting weather collector")
    data = fetch_weather_data()
    if data:
        save_weather_data(data)
    print("Weather data collection completed")

if __name__ =="__main__":
        main()
