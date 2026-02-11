from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
import os

from .routers import auth, cans
from .database import engine
from .models import Base

# Create database tables
Base.metadata.create_all(bind=engine)

app = FastAPI(title="Coca-Cola Collection API")

# CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173", "http://localhost:80"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Serve uploaded images as static files
UPLOAD_DIR = "/app/uploads"
os.makedirs(UPLOAD_DIR, exist_ok=True)
app.mount("/uploads", StaticFiles(directory=UPLOAD_DIR), name="uploads")

# Include routers
app.include_router(auth.router)
app.include_router(cans.router)

@app.get("/")
async def root():
    return {"message": "Coca-Cola Collection API is running!"}

@app.get("/api/health")
async def health_check():
    return {"status": "healthy"}