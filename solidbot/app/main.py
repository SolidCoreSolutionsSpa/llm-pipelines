# app/main.py
from fastapi import FastAPI
from app.api.endpoints import openai
from app.api.endpoints.openai import router
app = FastAPI()

app.include_router(openai.router, prefix="/api/v1", tags=["openai"])
app.include_router(router, prefix="/api/v1", tags=["openai"])

@app.get("/")
def read_root():
    return {"message": "Welcome to the OpenAI API"}
