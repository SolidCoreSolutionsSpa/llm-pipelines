from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, func,desc,asc
from app.models.sii_rag import Document
from pgvector.sqlalchemy import Vector
from app.core.config.logger import logger

class DocumentService:
    @staticmethod
    async def find_similar_embeddings(session: AsyncSession, query_embedding: Vector, limit=5):
        try:
            similarity_threshold = 0.8
            query = select(Document, Document.embedding.cosine_distance(query_embedding).label("distance")) \
                .filter(Document.embedding.cosine_distance(query_embedding) < similarity_threshold) \
                .order_by(asc("distance")) \
                .limit(limit)
            
            logger.info(f"Executing query: {query}")
            result = await session.execute(query)
            return result.all()
        except Exception as e:
            logger.error(f"Error in find_similar_embeddings: {str(e)}")
            raise

document_service = DocumentService()