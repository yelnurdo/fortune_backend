from pydantic import BaseModel
from datetime import datetime
from typing import List, Dict, Optional

class UserBase(BaseModel):
    name: str
    birthdate: datetime
    location: str
    birth_time: Optional[str] = None
    interests: str

    class Config:
        from_attributes = True

class UserCreate(UserBase):
    pass

class User(UserBase):
    id: int

    class Config:
        from_attributes = True

class PredictionCreate(BaseModel):
    user_id: int
    type: str
    additional_info: Dict[str, str]

class PredictionResult(BaseModel):
    images: List[str]
    text: str
    audio: str

class Prediction(BaseModel):
    id: int
    type: str
    result: PredictionResult

    class Config:
        from_attributes = True
