from pydantic import BaseModel

class TextGenerationRequest(BaseModel):
    prompt: str
    max_tokens: int

class TextGenerationResponse(BaseModel):
    text: str

class EmbeddingRequest(BaseModel):
    input_filename: str