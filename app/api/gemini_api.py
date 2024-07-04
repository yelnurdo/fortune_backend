import os
import requests
from dotenv import load_dotenv
import logging

load_dotenv()

GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")
GEMINI_API_URL = "https://aistudio.googleapis.com/v1/text:generate"  # Adjust this to the correct URL from Google's documentation

logger = logging.getLogger(__name__)

def get_prediction_text(prompt: str) -> str:
    headers = {
        "Authorization": f"Bearer {GEMINI_API_KEY}",
        "Content-Type": "application/json",
    }
    data = {
        "model": "gemini-1.5",  # Adjust if needed based on the API documentation
        "prompt": prompt,
        "max_tokens": 200,
        "temperature": 0.7
    }

    response = requests.post(GEMINI_API_URL, headers=headers, json=data)
    
    if response.status_code == 200:
        return response.json()['choices'][0]['message']['content'].strip()
    else:
        logger.error(f"Failed to generate text: {response.text}")
        raise Exception(f"Failed to generate text: {response.text}")
