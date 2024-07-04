import os
import cohere
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

# Get the Cohere API key from the environment variables
COHERE_API_KEY = os.getenv("COHERE_API_KEY")

# Initialize the Cohere client with the API key
cohere_client = cohere.Client(COHERE_API_KEY)

def get_prediction_text(prompt: str) -> str:
    """
    Generate a prediction text using the Cohere API.

    Parameters:
        prompt (str): The input text prompt to generate predictions.

    Returns:
        str: The generated prediction text.
    """
    try:
        # Call the Cohere API to generate text based on the prompt
        response = cohere_client.generate(
            model='command-xlarge-nightly',  # Используйте правильную модель, доступную вам
            prompt=prompt,
            max_tokens=200,
            temperature=0.7,
        )
        # Return the generated text
        return response.generations[0].text.strip()
    except Exception as e:
        # Raise an exception if text generation fails
        raise Exception(f"Failed to generate text: {e}")
