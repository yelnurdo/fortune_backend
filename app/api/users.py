from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from .. import crud, schemas
from ..dependencies import get_db_session
import logging

router = APIRouter()

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

@router.post("/", response_model=schemas.User)
def create_user(user: schemas.UserCreate, db: Session = Depends(get_db_session)):
    try:
        db_user = crud.get_user_by_name(db, name=user.name)
        if db_user:
            logger.info(f"User {user.name} already registered.")
            return schemas.User.from_orm(db_user)
        new_user = crud.create_user(db=db, user=user)
        return schemas.User.from_orm(new_user)
    except Exception as e:
        logger.error(f"Error creating user: {e}")
        raise HTTPException(status_code=500, detail=str(e))
