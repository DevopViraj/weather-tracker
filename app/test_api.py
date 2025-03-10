import os
import requests
from dotenv import load_dotenv

load_dotenv()

API_KEY = os.getenv("OPENWEATHER_API_KEY")
CITY_ID = "5128581"  # New York

url = f"https://api.openweathermap.org/data/2.5/weather?id={CITY_ID}&appid={API_KEY}&units=metric"
response = requests.get(url)

if response.status_code == 200:
    print("✅ API is working!")
    print(response.json())  # Print sample data
else:
    print(f"❌ API request failed! Status Code: {response.status_code}")
