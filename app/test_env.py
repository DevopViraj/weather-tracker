import os
from dotenv import load_dotenv

load_dotenv()

print("API Key:", os.getenv("OPENWEATHER_API_KEY"))
print("City IDs:", os.getenv("CITY_IDS"))
