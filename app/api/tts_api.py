import os
import requests
import json
from dotenv import load_dotenv
import logging
import uuid
import time

load_dotenv()

HUGGINGFACE_API_KEY = os.getenv("HUGGINGFACE_API_KEY")

logger = logging.getLogger(__name__)

def text_to_speech(text: str, retries: int = 5, delay: int = 30) -> str:
    headers = {
        "Authorization": f"Bearer {HUGGINGFACE_API_KEY}",
        "Content-Type": "application/json",
    }
    data = {
        "inputs": text,
    }

    for attempt in range(retries):
        response = requests.post(
            "https://api-inference.huggingface.co/models/facebook/fastspeech2-en-ljspeech",
            headers=headers,
            data=json.dumps(data),
        )

        if response.status_code == 200:
            logger.info("Saving audio")
            # Define the absolute path to the 'static' directory inside 'backend/app'
            static_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'static'))
            if not os.path.exists(static_dir):
                os.makedirs(static_dir)

            audio_filename = f"{uuid.uuid4()}.mp3"
            audio_path = os.path.join(static_dir, audio_filename)

            with open(audio_path, "wb") as audio_file:
                audio_file.write(response.content)

            logger.info(f"Audio saved at {audio_path}")
            # Log file creation details
            logger.info(f"File created: {audio_path}, Exists: {os.path.exists(audio_path)}")
            return f"/static/{audio_filename}"
        elif response.status_code == 503:
            logger.warning(f"Model is loading, retrying in {delay} seconds...")
            time.sleep(delay)
        else:
            logger.error(f"Failed to generate audio: {response.text}")
            raise Exception(f"Failed to generate audio: {response.text}")

    raise Exception("Model is still loading after multiple attempts")
