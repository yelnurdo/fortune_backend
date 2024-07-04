import os
import requests
from dotenv import load_dotenv
import logging

load_dotenv()

GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")
GEMINI_API_URL = "https://api.gemini.com/v1/predictions"
logger = logging.getLogger(__name__)


def get_prediction_text(prompt: str) -> str:
    headers = {
        "Authorization": f"Bearer {GEMINI_API_KEY}",
        "Content-Type": "application/json",
    }
    data = {
        "prompt": prompt,
        "max_tokens": 200,
        "n": 1,
        "temperature": 0.7,
    }

    try:
        response = requests.post(GEMINI_API_URL, headers=headers, json=data)
        response.raise_for_status()
        return response.json()['choices'][0]['text'].strip()
    except Exception as e:
        logger.error(f"Error fetching prediction text: {e}")
        return "Failed to fetch prediction text"
