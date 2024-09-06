import openai
from app.config import settings
from fastapi import HTTPException
from app.core.config.logger import logger

class OpenAIClient:
    def __init__(self, entity_type: str):
        self.api_key = settings.OPENAI_API_KEY
        openai.api_key = self.api_key
        self.system_prompt = f"""
                        Eres un experto en {entity_type} que proporciona información detallada en formato JSON.
                        Cada entidad debe tener dos campos: 'nombre' y 'descripcion'.
                        """
        self.entity_embeddings_file = f'app/data/{entity_type}_embs.json'

    def generate_text(self, prompt: str, max_tokens: int = 50, min_similarity: float = 0.9):
        try:
            response = openai.chat.completions.create(
                model="gpt-4",
                messages=[
                    {"role": "system", "content": self.system_prompt},
                    {"role": "user", "content": prompt}
                ],
                max_tokens=max_tokens
            )
            generated_text = response.choices[0].message.content
            logger.info("Generated Text:", generated_text)  # Depuración: Imprimir el texto generado
        except Exception as e:
            logger.error(f"OpenAI API Error: {e}")
            raise HTTPException(status_code=400, detail=f"OpenAI API Error: {e}")