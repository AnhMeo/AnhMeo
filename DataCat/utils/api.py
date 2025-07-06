import os
import requests
from dotenv import load_dotenv

# Load the API key from the .env file
load_dotenv()
API_KEY = os.getenv("VALORANT_API_KEY")
HEADERS = {"TRN-Api-Key": API_KEY}

def get_match_history(name: str, tag: str):
    
    encoded_tag = tag.replace("#", "%23")
    url = f"https://public-api.tracker.gg/v2/valorant/standard/profile/riot/AnhMeo%23iuMai"

    response = requests.get(url, headers=HEADERS)

    if response.status_code == 200:
        return response.json()
    else:
        print(f"Error {response.status_code}: {response.text}")
        return None
