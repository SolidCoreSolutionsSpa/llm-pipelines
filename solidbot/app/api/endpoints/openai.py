# app/api/endpoints/openai.py
from fastapi import APIRouter, HTTPException
from app.models.openai_models import OpenAIModel
from app.schemas.openai_schemas import TextGenerationRequest, TextGenerationResponse
from app.utils.openai_utils import embeddingManager
from pydantic import BaseModel

router = APIRouter()

@router.post("/generate-text", response_model=TextGenerationResponse)
def generate_text(request: TextGenerationRequest):
    openai_model = OpenAIModel()
    try:
        result = openai_model.generate_text(request.prompt, request.max_tokens)
        return result
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))


class EmbeddingRequest(BaseModel):
    input_filename: str
    output_filename: str

@router.post("/generate-embeddings")
def generate_embeddings(request: EmbeddingRequest):
    try:
        input_file = f'app/data/{request.input_filename}'
        output_file = f'app/data/{request.output_filename}'
        result = embeddingManager.process_and_save_embeddings(input_file, output_file)
        return result
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))