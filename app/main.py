import os
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from .database import engine, Base
from .api import users, predictions

Base.metadata.create_all(bind=engine)

app = FastAPI()

# CORS Configuration
origins = [
    "http://localhost:3000",
    "http://localhost:8000",
    "https://fortune-frontend-eta.vercel.app",  # Your Vercel frontend URL
    "https://fortunebackend-production.up.railway.app",  # Your Railway backend URL
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(users.router, prefix="/users", tags=["users"])
app.include_router(predictions.router, prefix="/predictions", tags=["predictions"])

# Define the absolute path to the 'static' directory inside 'backend/app'
static_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), 'static'))
if not os.path.exists(static_dir):
    os.makedirs(static_dir)
app.mount("/static", StaticFiles(directory=static_dir), name="static")

@app.get("/")
def read_root():
    return {"message": "Welcome to the History Book AI API"}
