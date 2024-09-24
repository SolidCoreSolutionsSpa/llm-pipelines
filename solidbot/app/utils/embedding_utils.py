import httpx
from app.core.config import settings

async def generate_embeddings(texts: list[str]) -> list[list[float]]:
    async with httpx.AsyncClient() as client:
        embeddings = []
        for text in texts:
            payload = {
                "model": settings.settings.EMBEDDING_MODEL,
                "input": text
            }
            response = await client.post(str(settings.settings.EMBEDDING_API_URL), json=payload)
            if response.status_code == 200:
                result = response.json()
                embeddings.append(result['data'][0]['embedding'])
            else:
                raise Exception(f"Error generating embedding: {response.text}")
        return embeddings