from pathlib import Path

from fastapi import FastAPI
from fastapi.responses import FileResponse
from fastapi.staticfiles import StaticFiles
from app.services.find_model import find_model


BASE_DIR = Path(__file__).resolve().parent
STATIC_DIR = BASE_DIR / "static"


app = FastAPI(title="FastAPI Sketchfab Finder")
app.mount("/static", StaticFiles(directory=STATIC_DIR), name="static")


@app.get("/api/health")
def health_check():
    return {"status": "ok"}


@app.get("/api/message")
def message():
    return {"message": "FastAPI backend is running."}


@app.get("/api/find-model")
def get_model(query: str):
    return find_model(query)


@app.get("/")
def index():
    return FileResponse(STATIC_DIR / "index.html")
