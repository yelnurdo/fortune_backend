from sqlalchemy.orm import Session
from . import models, schemas

def get_user(db: Session, user_id: int):
    return db.query(models.User).filter(models.User.id == user_id).first()

def get_user_by_name(db: Session, name: str):
    return db.query(models.User).filter(models.User.name == name).first()

def create_user(db: Session, user: schemas.UserCreate):
    db_user = models.User(
        name=user.name,
        birthdate=user.birthdate,
        location=user.location,
        birth_time=user.birth_time,
        interests=user.interests
    )
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user

def create_prediction(db: Session, prediction: schemas.PredictionCreate, result: schemas.PredictionResult):
    db_prediction = models.Prediction(
        user_id=prediction.user_id,
        type=prediction.type,
        additional_info=prediction.additional_info,
        result=result.dict()  # сохраняем результат как JSON
    )
    db.add(db_prediction)
    db.commit()
    db.refresh(db_prediction)
    return db_prediction
