from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from .. import crud, schemas
from ..dependencies import get_db_session
from .cohere_api import get_prediction_text
from .image_generation_api import generate_cartoon_image
from .tts_api import text_to_speech
import logging

router = APIRouter()

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def generate_image_prompts(story: str) -> list:
    lines = story.split('\n')
    prompts = [f"A depiction of: {line.strip()}" for line in lines if line.strip()]
    return prompts

@router.post("/", response_model=schemas.Prediction)
def create_prediction(
    prediction: schemas.PredictionCreate, 
    db: Session = Depends(get_db_session)
):
    try:
        logger.info("Generating prediction text")

        user_info = prediction.additional_info
        prompt = f"As a fortune teller, I see that the user has the following details: {user_info}. Please provide a detailed prediction."
        story = get_prediction_text(prompt)

        if not story:
            raise HTTPException(status_code=500, detail="Failed to generate prediction text")

        image_prompts = generate_image_prompts(story)
        images = [generate_cartoon_image(prompt) for prompt in image_prompts]

        audio_url = text_to_speech(story)

        result = schemas.PredictionResult(
            images=images,
            text=story,
            audio=audio_url
        )

        db_prediction = crud.create_prediction(db=db, prediction=prediction, result=result)
        return db_prediction
    except Exception as e:
        logger.error(f"Error creating prediction: {e}")
        raise HTTPException(status_code=500, detail=str(e))
