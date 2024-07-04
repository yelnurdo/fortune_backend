from sqlalchemy import Column, Integer, String, ForeignKey, JSON
from sqlalchemy.orm import relationship
from .database import Base

class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, index=True)
    birthdate = Column(String)
    location = Column(String)
    birth_time = Column(String, nullable=True)
    interests = Column(String)

class Prediction(Base):
    __tablename__ = "predictions"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey('users.id'))
    type = Column(String, index=True)
    additional_info = Column(JSON)
    result = Column(JSON)  # добавляем поле result
    user = relationship("User", back_populates="predictions")

User.predictions = relationship("Prediction", back_populates="user")
