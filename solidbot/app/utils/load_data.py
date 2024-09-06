import json
import asyncio
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import sessionmaker
from core.config.database import create_engine
from models.sii_rag import Document, TemaLink, RespuestaLink, PreguntaRelacionada
from solidbot.app.core.config.settings import settings
from sentence_transformers import SentenceTransformer

# Inicializar el modelo de embedding
model = SentenceTransformer('paraphrase-multilingual-MiniLM-L12-v2')

async def generate_embeddings(texts: list[str]) -> list[list[float]]:
    # SentenceTransformer no es asíncrono, así que lo ejecutamos en un thread separado
    embeddings = await asyncio.to_thread(model.encode, texts)
    return embeddings.tolist()

async def load_documents_batch(session: AsyncSession, items: list[dict]):
    texts = [f"{item['tema']['texto']} {item['pregunta']['texto']} {item['respuesta']['texto']}" for item in items]
    embeddings = await generate_embeddings(texts)

    for item, embedding in zip(items, embeddings):
        doc = Document(
            source=item.get('source', ''),
            tema_texto=item['tema']['texto'],
            pregunta_id=item['pregunta']['id'],
            pregunta_fecha_creacion=item['pregunta']['fecha_creacion'],
            pregunta_texto=item['pregunta']['texto'],
            respuesta_fecha_actualizacion=item['respuesta']['fecha_actualizacion'],
            respuesta_texto=item['respuesta']['texto'],
            embedding=embedding
        )
        session.add(doc)

        for link in item['tema']['links']:
            tema_link = TemaLink(texto=link['texto'], href=link['href'])
            doc.tema_links.append(tema_link)

        for link in item['respuesta']['links']:
            respuesta_link = RespuestaLink(texto=link['texto'], href=link['href'])
            doc.respuesta_links.append(respuesta_link)

        for pregunta in item['preguntas_relacionadas']:
            pregunta_relacionada = PreguntaRelacionada(texto=pregunta['texto'], href=pregunta['href'])
            doc.preguntas_relacionadas.append(pregunta_relacionada)

    await session.commit()

async def main():
    engine = create_engine()
    async_session = sessionmaker(engine, class_=AsyncSession, expire_on_commit=False)

    async with async_session() as session:
        with open('data.json', 'r', encoding='utf-8') as file:
            data = json.load(file)

        batch_size = 100  # Podemos aumentar el tamaño del batch debido al embedding más pequeño
        for i in range(0, len(data), batch_size):
            batch = data[i:i+batch_size]
            await load_documents_batch(session, batch)
            print(f"Processed batch {i//batch_size + 1}")

    print("Data loading completed.")

if __name__ == "__main__":
    asyncio.run(main())