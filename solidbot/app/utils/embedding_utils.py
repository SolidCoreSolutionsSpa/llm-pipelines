import asyncio
from sentence_transformers import SentenceTransformer

# Initialize the embedding model
model = SentenceTransformer('paraphrase-multilingual-MiniLM-L12-v2')

async def generate_embeddings(texts: list[str]) -> list[list[float]]:
    embeddings = await asyncio.to_thread(model.encode, texts)
    return embeddings.tolist()