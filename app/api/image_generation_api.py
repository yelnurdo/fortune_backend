import os
import requests
from dotenv import load_dotenv
import logging
import uuid
import time

load_dotenv()

CARTOON_API_URL = "https://api-inference.huggingface.co/models/alvdansen/midsommarcartoon"
HUGGINGFACE_API_KEY = os.getenv("HUGGINGFACE_API_KEY")

logger = logging.getLogger(__name__)

def generate_cartoon_image(prompt: str) -> str:
    headers = {
        "Authorization": f"Bearer {HUGGINGFACE_API_KEY}",
    }
    try:
        for attempt in range(5):
            response = requests.post(CARTOON_API_URL, headers=headers, json={"inputs": prompt})
            if response.status_code == 200:
                # Define the absolute path to the 'static' directory inside 'backend/app'
                static_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'static'))
                if not os.path.exists(static_dir):
                    os.makedirs(static_dir)

                image_filename = f"{uuid.uuid4()}.jpg"
                image_path = os.path.join(static_dir, image_filename)

                with open(image_path, "wb") as f:
                    f.write(response.content)

                logger.info(f"Image saved at {image_path}")
                # Log file creation details
                logger.info(f"File created: {image_path}, Exists: {os.path.exists(image_path)}")
                return f"/static/{image_filename}"
            elif response.status_code == 503:
                logger.warning(f"Model is loading, retrying in 30 seconds...")
                time.sleep(30)
            else:
                logger.error(f"Failed to generate image: {response.text}")
                return "Failed to generate image"

        logger.error("Model is still loading after multiple attempts")
        return "Model is still loading, please try again later."
    except Exception as e:
        logger.error(f"Exception while generating image: {e}")
        return "Failed to generate image"
