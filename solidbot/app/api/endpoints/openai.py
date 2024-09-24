# app/api/endpoints/openai.py
from fastapi import APIRouter, HTTPException,Depends
from app.models.openai_models import OpenAIModel
from app.schemas.openai_schemas import TextGenerationRequest, TextGenerationResponse
from app.utils.openai_utils import embeddingManager
from pydantic import BaseModel
from fastapi import APIRouter, HTTPException, BackgroundTasks
from app.api.services.embedding_service import process_embeddings
from app.api.services.document_service import document_service
from app.core.config.database import get_async_db, AsyncSession
from app.utils.embedding_utils import generate_embeddings as gen_emb
from app.core.config.logger import logger
from pgvector.sqlalchemy import Vector
import numpy as np

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
    
@router.post("/save-embeddings")
async def save_embeddings( background_tasks: BackgroundTasks):
    try:
        # input_file = f'app/data/{request.input_filename}'
        background_tasks.add_task(process_embeddings)
        return {"message": "Embedding generation started in the background"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/documents")
async def get_documents(question: str, db: AsyncSession = Depends(get_async_db)):
    try:
        logger.info(f"Received question: {question}")
        question_embeddings = await gen_emb([question])
        
        question_embedding = question_embeddings[0]
        
        similar_documents = await document_service.find_similar_embeddings(db, question_embedding)
        
        results = []
        for doc, distance in similar_documents:
            results.append({
                "id": doc.id,
                "distance": distance,
                "pregunta_texto": doc.pregunta_texto,
                "respuesta_texto": doc.respuesta_texto,
                "similarity": 1 - distance
            })
        
        return {"results": results}
    except Exception as e:
        logger.error(f"Error in get_documents: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))
