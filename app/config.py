import os
from dotenv import load_dotenv

load_dotenv()

OPENWEATHER_API_KEY = os.getenv("OPENWEATHER_API_KEY")
CITY_IDS = os.getenv("CITY_IDS")

DATA_DIRECTORY = os.path.join(os.path.dirname(__file__), 'data')