from pydantic import BaseModel
from typing import Optional, Union


class TextGenerationRequest(BaseModel):
    prompt: str
    max_tokens: Optional[int] = 50
    min_similarity: Optional[float] = 0.8

class TextGenerationResponse(BaseModel):
    # receta: RecipeResponse
    product_ids: list[int | None]

